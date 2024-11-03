from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Type

from pccontext.enums import Era, HistoryType, Network, TransactionType
from pccontext.models import BaseModel
from pccontext.utils import DATE_FORMAT_2, check_file_exists, dump_file, load_json_file

from .address_info_model import AddressInfo
from .genesis_parameters_model import GenesisParameters
from .protocol_parameters_model import ProtocolParameters
from .token_metadata_model import TokenMetadata

__all__ = [
    "OfflineTransferGeneral",
    "OfflineTransferProtocol",
    "OfflineTransferHistory",
    "OfflineTransferFile",
    "OfflineTransferTransaction",
    "OfflineTransfer",
    "TransactionJSON",
]


@dataclass(frozen=True)
class OfflineTransferGeneral(BaseModel):
    """
    Offline transfer json file general property model class
    """

    offline_cli_version: Optional[str] = field(
        default=None,
        metadata={"aliases": ["offline_cli_version", "offlineCliVersion"]},
    )
    online_cli_version: Optional[str] = field(
        default=None,
        metadata={"aliases": ["online_cli_version", "onlineCliVersion"]},
    )
    online_node_version: Optional[str] = field(
        default=None,
        metadata={"aliases": ["online_node_version", "onlineNodeVersion"]},
    )


@dataclass(frozen=True)
class OfflineTransferProtocol(BaseModel):
    """
    Offline transfer json file protocol property model class
    """

    protocol_parameters: Optional[ProtocolParameters] = None
    genesis_parameters: Optional[GenesisParameters] = None
    era: Optional[Era] = None
    network: Optional[Network] = None

    @classmethod
    def property_from_dict(
        cls: Type[OfflineTransferProtocol],
        value: Dict,
        key: str,
        field_name: str,
        init_args: Dict,
    ):
        """
        Parse the property from a dictionary
        :param value: The value
        :param key: The key
        :param field_name: The field name
        :param init_args: The initialization arguments
        :return: The property
        """
        if field_name == "protocol_parameters":
            return ProtocolParameters.from_dict(value)
        elif field_name == "genesis_parameters":
            return GenesisParameters.from_dict(value)


@dataclass(frozen=True)
class OfflineTransferHistory(BaseModel):
    """
    Offline transfer json file history property model class
    """

    date: Optional[str] = field(
        default=datetime.now(timezone.utc).strftime(DATE_FORMAT_2)
    )
    action: Optional[str] = None


@dataclass(frozen=True)
class OfflineTransferFile(BaseModel):
    """
    Offline transfer json file property model class
    """

    name: Optional[str] = None
    date: Optional[str] = field(
        default=datetime.now(timezone.utc).strftime(DATE_FORMAT_2)
    )
    size: Optional[int] = None
    base64: Optional[bytes] = None


@dataclass(frozen=True)
class TransactionJSON(BaseModel):
    """
    Offline transfer json file property model class
    """

    type: Optional[str] = None
    description: Optional[str] = None
    cborHex: Optional[str] = None


@dataclass(frozen=True)
class OfflineTransferTransaction(BaseModel):
    """
    Offline transfer json transaction property model class
    """

    type: Optional[TransactionType] = None
    date: Optional[str] = field(
        default=datetime.now(timezone.utc).strftime(DATE_FORMAT_2)
    )
    era: Optional[Era] = None
    stake_address: Optional[str] = field(
        default=None,
        metadata={"aliases": ["stake_address", "stakeAddress"]},
    )
    from_address: Optional[str] = field(
        default=None,
        metadata={"aliases": ["from_address", "fromAddress"]},
    )
    from_name: Optional[str] = field(
        default=None,
        metadata={"aliases": ["from_name", "fromName"]},
    )
    to_address: Optional[str] = field(
        default=None,
        metadata={"aliases": ["to_address", "toAddress"]},
    )
    to_name: Optional[str] = field(
        default=None,
        metadata={"aliases": ["to_name", "toName"]},
    )
    tx_json: Optional[TransactionJSON] = field(
        default=None,
        metadata={"aliases": ["tx_json", "txJson"]},
    )

    @classmethod
    def property_from_dict(
        cls: Type[OfflineTransferTransaction],
        value: Dict,
        key: str,
        field_name: str,
        init_args: Dict,
    ):
        """
        Parse the property from a dictionary
        :param value: The value
        :param key: The key
        :param field_name: The field name
        :param init_args: The initialization arguments
        :return: The property
        """
        if field_name == "tx_json":
            return TransactionJSON.from_dict(value)


@dataclass(frozen=True)
class OfflineTransfer(BaseModel):
    """
    Offline transfer json file model class
    """

    general: Optional[OfflineTransferGeneral] = None
    protocol: Optional[OfflineTransferProtocol] = None
    history: List[OfflineTransferHistory] = field(default_factory=list)
    files: List[OfflineTransferFile] = field(default_factory=list)
    transactions: List[OfflineTransferTransaction] = field(default_factory=list)
    addresses: List[AddressInfo] = field(default_factory=list)
    token_meta_server: List[TokenMetadata] = field(
        default_factory=list,
        metadata={"aliases": ["token_meta_server", "tokenMetaServer"]},
    )

    def __post_init__(self):
        if self.general is None:
            object.__setattr__(self, "general", OfflineTransferGeneral())

        if self.protocol is None:
            object.__setattr__(self, "protocol", OfflineTransferProtocol())

        # if self.addresses is not None:
        #     object.__setattr__(self, "addresses", [AddressInfo()])

    @classmethod
    def property_from_dict(
        cls: Type[OfflineTransfer],
        value: Dict,
        key: str,
        field_name: str,
        init_args: Dict,
    ):
        """
        Parse the property from a dictionary
        :param value: The value
        :param key: The key
        :param field_name: The field name
        :param init_args: The initialization arguments
        :return: The property
        """
        if field_name == "general":
            return OfflineTransferGeneral.from_dict(value)
        elif field_name == "protocol":
            return OfflineTransferProtocol.from_dict(value)
        elif field_name == "history":
            return OfflineTransferHistory.from_dict(value)
        elif field_name == "files":
            return OfflineTransferFile.from_dict(value)
        elif field_name == "transactions":
            return OfflineTransferTransaction.from_dict(value)
        elif field_name == "addresses":
            return AddressInfo.from_dict(value)
        elif field_name == "token_meta_server":
            return TokenMetadata.from_dict(value)

    @staticmethod
    def new(offline_file_path: Path) -> OfflineTransfer:
        """
        Build a fresh new offlineJSON with the current protocolParameters in it

        :param offline_file_path: The offline file path
        :return: None
        """

        offline_json = {
            "general": {
                "online_cli_version": None,
                "online_node_version": None,
            },
            "protocol": {
                "protocol_parameters": None,
                "era": None,
            },
            "history": [
                {
                    "date": datetime.now(timezone.utc),
                    "action": HistoryType.NEW.value,
                }
            ],
        }

        new_offline_transfer = OfflineTransfer.from_json(offline_json)

        dump_file(
            offline_file_path,
            new_offline_transfer.to_json(),
        )

        return new_offline_transfer

    @staticmethod
    def check(offline_transfer_file: Path) -> None:
        """
        Check that the offlineTransfer.json file exist
        :param offline_transfer_file: The offline transfer file
        :return: None
        """
        try:
            check_file_exists(offline_transfer_file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Offline transfer file is not a file or does not exist: "
                f"{offline_transfer_file.as_posix()}"
            )
            # print(
            #     f"[yellow]Offline transfer file is not a file or does not exist: "
            #     f"{offline_transfer_file.as_posix()}\n"
            #     f"Creating a new one...[/yellow]"
            # )
            # OfflineTransfer.new(offline_transfer_file)

    @staticmethod
    def load(offline_transfer_file: Path) -> OfflineTransfer:
        """
        Load the offline transfer file
        :param offline_transfer_file: The offline transfer file
        :return: The offline transfer file
        """
        OfflineTransfer.check(offline_transfer_file)
        return OfflineTransfer.from_json(load_json_file(offline_transfer_file))
