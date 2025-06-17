"""
Cardano CLI Chain Context
"""

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import List, Optional, Union

import cbor2
import docker
from cachetools import Cache, LRUCache, TTLCache, func
from docker.errors import APIError
from pycardano.address import Address
from pycardano.backend.base import ProtocolParameters as PyCardanoProtocolParameters
from pycardano.exception import (
    CardanoCliError,
    PyCardanoException,
    TransactionFailedException,
)
from pycardano.hash import DatumHash, ScriptHash
from pycardano.nativescript import NativeScript
from pycardano.network import Network as PyCardanoNetwork
from pycardano.plutus import (
    Datum,
    PlutusV1Script,
    PlutusV2Script,
    PlutusV3Script,
    RawPlutusData,
)
from pycardano.serialization import RawCBOR
from pycardano.transaction import (
    Asset,
    AssetName,
    MultiAsset,
    TransactionInput,
    TransactionOutput,
    UTxO,
    Value,
)
from pycardano.types import JsonDict

from pccontext.backend import ChainContext
from pccontext.enums import Network
from pccontext.models import GenesisParameters, ProtocolParameters, StakeAddressInfo

__all__ = ["CardanoCliChainContext", "DockerConfig"]


class DockerConfig:
    """
    Docker configuration to use the cardano-cli in a Docker container
    """

    container_name: str
    """ The name of the Docker container containing the cardano-cli"""

    host_socket: Optional[Path]
    """ The path to the Docker host socket file"""

    def __init__(self, container_name: str, host_socket: Optional[Path] = None):
        self.container_name = container_name
        self.host_socket = host_socket


class CardanoCliChainContext(ChainContext):
    _binary: Path
    _socket: Optional[Path]
    _config_file: Path
    _network: Network
    _last_known_block_slot: int
    _last_chain_tip_fetch: float
    _genesis_param: Optional[GenesisParameters]
    _protocol_param: Optional[ProtocolParameters]
    _utxo_cache: Cache
    _datum_cache: Cache
    _docker_config: Optional[DockerConfig]
    _network_magic_number: Optional[int]

    def __init__(
        self,
        binary: Path,
        socket: Path,
        config_file: Path,
        network: Network,
        refetch_chain_tip_interval: Optional[float] = None,
        utxo_cache_size: int = 10000,
        datum_cache_size: int = 10000,
        docker_config: Optional[DockerConfig] = None,
        network_magic_number: Optional[int] = None,
    ):
        if docker_config is None:
            if not binary.exists() or not binary.is_file():
                raise CardanoCliError(f"cardano-cli binary file not found: {binary}")

            # Check the socket path file and set the CARDANO_NODE_SOCKET_PATH environment variable
            try:
                if not socket.exists():
                    raise CardanoCliError(f"cardano-node socket not found: {socket}")
                elif not socket.is_socket():
                    raise CardanoCliError(f"{socket} is not a socket file")

                self._socket = socket
                os.environ["CARDANO_NODE_SOCKET_PATH"] = self._socket.as_posix()
            except CardanoCliError:
                self._socket = None

        self._binary = binary
        self._network = network
        self._config_file = config_file
        self._last_known_block_slot = 0
        self._refetch_chain_tip_interval = (
            refetch_chain_tip_interval
            if refetch_chain_tip_interval is not None
            else 1000
        )
        self._last_chain_tip_fetch = 0
        self._genesis_param = None
        self._protocol_param = None
        if refetch_chain_tip_interval is None:
            slot_length = self.genesis_param.slot_length or 1
            active_slots_coefficient = (
                self.genesis_param.active_slots_coefficient or 0.05
            )
            self._refetch_chain_tip_interval = float(
                slot_length / active_slots_coefficient
            )

        self._utxo_cache = TTLCache(
            ttl=self._refetch_chain_tip_interval, maxsize=utxo_cache_size
        )
        self._datum_cache = LRUCache(maxsize=datum_cache_size)
        self._docker_config = docker_config
        self._network_magic_number = network_magic_number

    @property
    def _network_args(self) -> List[str]:
        if self._network is Network.CUSTOM:
            return self._network.get_cli_network_args(self._network_magic_number)
        else:
            return self._network.get_cli_network_args()

    def _run_command(self, cmd: List[str]) -> str:
        """
        Runs the command in the cardano-cli. If the docker configuration is set, it will run the command in the
        docker container.

        :param cmd: Command as a list of strings
        :return: The stdout if the command runs successfully
        """
        try:
            if self._docker_config:
                docker_config = self._docker_config
                if docker_config.host_socket is None:
                    client = docker.from_env()
                else:
                    client = docker.DockerClient(
                        base_url=docker_config.host_socket.as_posix()
                    )

                container = client.containers.get(docker_config.container_name)

                exec_result = container.exec_run(
                    [self._binary.as_posix()] + cmd, stdout=True, stderr=True
                )

                if exec_result.exit_code == 0:
                    output = exec_result.output.decode()
                    return output
                else:
                    error = exec_result.output.decode()
                    raise CardanoCliError(error)
            else:
                result = subprocess.run(
                    [self._binary.as_posix()] + cmd, capture_output=True, check=True
                )
                return result.stdout.decode().strip()
        except subprocess.CalledProcessError as err:
            raise CardanoCliError(err.stderr.decode()) from err
        except APIError as err:
            raise CardanoCliError(err) from err

    def _query_chain_tip(self) -> JsonDict:
        result = self._run_command(["query", "tip"] + self._network_args)
        return json.loads(result)

    def _query_current_protocol_params(self) -> JsonDict:
        result = self._run_command(
            ["query", "protocol-parameters"] + self._network_args
        )
        return json.loads(result)

    def _query_genesis_config(self) -> GenesisParameters:
        return GenesisParameters.from_config_file(self._config_file)

    def _is_chain_tip_updated(self):
        # fetch at almost every twenty seconds!
        if time.time() - self._last_chain_tip_fetch < self._refetch_chain_tip_interval:
            return False
        self._last_chain_tip_fetch = time.time()
        result = self._query_chain_tip()
        return float(result["syncProgress"]) != 100.0

    def _fetch_protocol_param(self) -> ProtocolParameters:
        result = self._query_current_protocol_params()
        return ProtocolParameters.from_json(result)

    @property
    def protocol_param(self) -> PyCardanoProtocolParameters:
        """Get current protocol parameters"""
        if not self._protocol_param or self._is_chain_tip_updated():
            self._protocol_param = self._fetch_protocol_param()
        return self._protocol_param.to_pycardano()

    @property
    def genesis_param(self) -> GenesisParameters:
        """Get chain genesis parameters"""
        if not self._genesis_param:
            self._genesis_param = self._query_genesis_config()
        return self._genesis_param

    @property
    def network(self) -> PyCardanoNetwork:
        """Cet current network"""
        return self._network.get_network()

    @property
    def epoch(self) -> int:
        """Current epoch number"""
        result = self._query_chain_tip()
        return result["epoch"]

    @property
    def era(self) -> int:
        """Current Cardano era"""
        result = self._query_chain_tip()
        return result["era"]

    @property
    @func.ttl_cache(ttl=1)
    def last_block_slot(self) -> int:
        result = self._query_chain_tip()
        return result["slot"]

    def version(self):
        """
        Gets the cardano-cli version
        """
        return self._run_command(["version"])

    @staticmethod
    def _get_script(
        reference_script: dict,
    ) -> Union[PlutusV1Script, PlutusV2Script, NativeScript]:
        """
        Get a script object from a reference script dictionary.
        Args:
            reference_script:

        Returns:

        """
        script_type = reference_script["script"]["type"]
        script_json: JsonDict = reference_script["script"]
        if script_type == "PlutusScriptV1":
            v1script = PlutusV1Script(
                cbor2.loads(bytes.fromhex(script_json["cborHex"]))
            )
            return v1script
        elif script_type == "PlutusScriptV2":
            v2script = PlutusV2Script(
                cbor2.loads(bytes.fromhex(script_json["cborHex"]))
            )
            return v2script
        elif script_type == "PlutusScriptV3":
            v3script = PlutusV3Script(
                cbor2.loads(bytes.fromhex(script_json["cborHex"]))
            )
            return v3script
        else:
            return NativeScript.from_dict(script_json)

    def _utxos(self, address: str) -> List[UTxO]:
        """Get all UTxOs associated with an address.

        Args:
            address (str): An address encoded with bech32.

        Returns:
            List[UTxO]: A list of UTxOs.
        """
        key = (self.last_block_slot, address)
        if key in self._utxo_cache:
            return self._utxo_cache[key]

        result = self._run_command(
            ["query", "utxo", "--address", address, "--out-file", "/dev/stdout"]
            + self._network_args
        )

        raw_utxos = json.loads(result)

        utxos = []
        for tx_hash in raw_utxos.keys():
            tx_id, tx_idx = tx_hash.split("#")
            utxo = raw_utxos[tx_hash]
            tx_in = TransactionInput.from_primitive([tx_id, int(tx_idx)])

            value = Value()
            multi_asset = MultiAsset()
            for asset in utxo["value"].keys():
                if asset == "lovelace":
                    value.coin = utxo["value"][asset]
                else:
                    policy_id = asset
                    policy = ScriptHash.from_primitive(policy_id)

                    for asset_hex_name in utxo["value"][asset].keys():
                        asset_name = AssetName.from_primitive(asset_hex_name)
                        amount = utxo["value"][asset][asset_hex_name]
                        multi_asset.setdefault(policy, Asset())[asset_name] = amount

            value.multi_asset = multi_asset

            datum_hash = (
                DatumHash.from_primitive(utxo["datumhash"])
                if utxo.get("datumhash") is not None
                else None
            )

            datum: Optional[Datum] = None

            if utxo.get("datum"):
                datum = RawCBOR(bytes.fromhex(utxo["datum"]))
            elif utxo.get("inlineDatumhash"):
                datum = RawPlutusData.from_dict(utxo["inlineDatum"])

            script = None

            if utxo.get("referenceScript"):
                script = self._get_script(utxo["referenceScript"])

            tx_out = TransactionOutput(
                Address.from_primitive(utxo["address"]),
                amount=value,
                datum_hash=datum_hash,
                datum=datum,
                script=script,
            )

            utxos.append(UTxO(tx_in, tx_out))

        self._utxo_cache[key] = utxos

        return utxos

    def submit_tx_cbor(self, cbor: Union[bytes, str]) -> str:
        """Submit a transaction to the blockchain.

        Args:
            cbor (Union[bytes, str]): The transaction to be submitted.

        Returns:
            str: The transaction hash.

        Raises:
            :class:`TransactionFailedException`: When fails to submit the transaction to blockchain.
            :class:`PyCardanoException`: When fails to retrieve the transaction hash.
        """
        if isinstance(cbor, bytes):
            cbor = cbor.hex()

        with tempfile.NamedTemporaryFile(mode="w") as tmp_tx_file:
            tx_json = {
                "type": f"Witnessed Tx {self.era}Era",
                "description": "Generated by PyCardano",
                "cborHex": cbor,
            }

            tmp_tx_file.write(json.dumps(tx_json))

            tmp_tx_file.flush()

            try:
                self._run_command(
                    [
                        "latest",
                        "transaction",
                        "submit",
                        "--tx-file",
                        tmp_tx_file.name,
                    ]
                    + self._network_args
                )
            except CardanoCliError:
                try:
                    self._run_command(
                        ["transaction", "submit", "--tx-file", tmp_tx_file.name]
                        + self._network_args
                    )
                except CardanoCliError as err:
                    raise TransactionFailedException(
                        "Failed to submit transaction"
                    ) from err

            # Get the transaction ID
            try:
                txid = self._run_command(
                    ["latest", "transaction", "txid", "--tx-file", tmp_tx_file.name]
                )
            except CardanoCliError:
                try:
                    txid = self._run_command(
                        ["transaction", "txid", "--tx-file", tmp_tx_file.name]
                    )
                except CardanoCliError as err:
                    raise PyCardanoException(
                        f"Unable to get transaction id for {tmp_tx_file.name}"
                    ) from err

        return txid

    def stake_address_info(self, stake_address: str) -> List[StakeAddressInfo]:
        """Get the stake address information.

        Args:
            stake_address (str): The stake address.

        Returns:
            List[StakeAddressInfo]: The stake address information.
        """

        result = self._run_command(
            [
                "query",
                "stake-address-info",
                "--address",
                stake_address,
                "--out-file",
                "/dev/stdout",
            ]
            + self._network_args
        )

        info = json.loads(result)

        return [
            StakeAddressInfo(
                address=stake_address,
                delegation_deposit=rewards_state.get("delegationDeposit", None),
                stake_delegation=rewards_state.get("stakeDelegation", None),
                reward_account_balance=rewards_state.get("rewardAccountBalance", None),
                vote_delegation=rewards_state.get("voteDelegation", None),
            )
            for rewards_state in info
        ]
