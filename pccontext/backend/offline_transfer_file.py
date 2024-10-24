from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Union

from pycardano import ChainContext, Network
from pycardano import ProtocolParameters as PyCardanoProtocolParameters
from pycardano import Transaction, UTxO

from pccontext.enums import Era, HistoryType, TransactionType
from pccontext.exceptions import OfflineTransferFileError
from pccontext.models import (
    GenesisParameters,
    OfflineTransfer,
    OfflineTransferHistory,
    OfflineTransferTransaction,
    ProtocolParameters,
    StakeAddressInfo,
)
from pccontext.models.offline_transfer_model import TransactionJSON
from pccontext.utils import check_file_exists, dump_file, load_json_file

__all__ = ["OfflineTransferFileContext"]


class OfflineTransferFileContext(ChainContext):
    """
    Offline transfer file context. To be used with the offline transfer file.
    """

    _offline_transfer_file: Path
    """Path to the offline transfer file"""

    _offline_transfer: OfflineTransfer
    """Offline transfer file object model"""

    _genesis_param: Optional[GenesisParameters]
    """Genesis parameters"""

    _protocol_param: Optional[ProtocolParameters]
    """Protocol parameters"""

    def __init__(
        self,
        offline_transfer_file: Path,
    ):
        super().__init__()
        self._offline_transfer_file = offline_transfer_file
        self._genesis_param = None
        self._protocol_param = None
        self._offline_transfer = self.load()

    @property
    def offline_transfer(self) -> OfflineTransfer:
        """
        Get the offline transfer file
        :return: The offline transfer file
        """
        return self._offline_transfer

    def check(self) -> None:
        """
        Check that the offlineTransfer.json file exist
        :return: None
        """
        try:
            check_file_exists(self._offline_transfer_file)
        except FileNotFoundError:
            print(
                f"Offline transfer file is not a file or does not exist: "
                f"{self._offline_transfer_file.as_posix()}\n"
                f"Creating a new one..."
            )
            OfflineTransfer.new(self._offline_transfer_file)

    def load(self) -> OfflineTransfer:
        """
        Load the offline transfer file
        :return: The offline transfer file
        """
        try:
            self.check()
            return OfflineTransfer.from_json(
                load_json_file(self._offline_transfer_file)
            )
        except FileNotFoundError as e:
            raise OfflineTransferFileError(
                f"Offline transfer file does not exist: {self._offline_transfer_file}"
            ) from e

    def _fetch_protocol_param(self) -> ProtocolParameters:
        if not self._offline_transfer.protocol:
            raise OfflineTransferFileError(
                "Protocol parameters not found in the offline transfer file."
            )
        result = self._offline_transfer.protocol.parameters
        if isinstance(result, ProtocolParameters):
            return result
        elif isinstance(result, dict):
            return ProtocolParameters.from_json(result)
        else:
            return ProtocolParameters(**result.__dict__)

    @property
    def protocol_param(self) -> PyCardanoProtocolParameters:
        """Get current protocol parameters"""
        if not self._protocol_param:
            self._protocol_param = self._fetch_protocol_param()
        return self._protocol_param.to_pycardano()

    @property
    def epoch(self) -> Union[int, None]:
        """Current epoch number"""
        if (
            self._offline_transfer.protocol
            and self._offline_transfer.protocol.parameters
        ):
            return self._offline_transfer.protocol.parameters.epoch
        return None

    @property
    def era(self) -> Optional[Era]:
        """Current Cardano era"""
        if self._offline_transfer.protocol:
            return self._offline_transfer.protocol.era
        return None

    @property
    def network(self) -> Optional[Network]:
        """Current Cardano network"""
        if self._offline_transfer.protocol:
            if (
                self._offline_transfer.protocol.network
                and self._offline_transfer.protocol.network.value == "mainnet"
            ):
                return Network.MAINNET
        return Network.TESTNET

    def _utxos(self, address: str) -> Optional[List[UTxO]]:
        """
        Get all UTxOs associated with an address.

        Args:
            address (str): An address encoded with bech32.

        Returns:
            List[UTxO]: A list of UTxOs or an empty list if the address is not found.
        """

        return next(
            (
                offline_address.utxos
                for offline_address in self._offline_transfer.addresses
                if address == str(offline_address.address)
            ),
            [],
        )

    def submit_tx_cbor(self, cbor: Union[bytes, str]):
        """Save the transaction to the offline transfer file.

        Args:
            cbor (Union[bytes, str]): The serialized transaction to be submitted.

        Raises:
            :class:`InvalidArgumentException`: When the transaction is invalid.
            :class:`TransactionFailedException`: When fails to submit the transaction to blockchain.
        """
        if isinstance(cbor, bytes):
            cbor = cbor.hex()

        tx_json = TransactionJSON(
            f"Witnessed Tx {self.era}Era",
            "Generated by PyCardano",
            cbor,
        )

        tx = Transaction.from_cbor(cbor)
        offline_transaction = OfflineTransferTransaction(
            type=TransactionType.TRANSACTION,
            tx_json=tx_json,
        )

        action = HistoryType.SAVE_TRANSACTION.value(tx.id)

        self._offline_transfer.transactions.append(offline_transaction)
        self._offline_transfer.history.append(OfflineTransferHistory(action=action))

        dump_file(
            self._offline_transfer_file,
            self._offline_transfer.to_json(),
        )

    def stake_address_info(self, stake_address: str) -> List[StakeAddressInfo]:
        """Get the stake address information.

        Args:
            stake_address (str): The stake address.

        Returns:
            List[StakeAddressInfo]: The stake address information.
        """

        # select stake_address_info from the addresses in the offline transfer file that match the stake_address
        return next(
            (
                offline_address.stake_address_info or []
                for offline_address in self._offline_transfer.addresses
                if offline_address.stake_address_info
                and any(
                    stake_address == stake_info.address
                    for stake_info in offline_address.stake_address_info
                )
            ),
            [],
        )
