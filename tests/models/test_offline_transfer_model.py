import json

from pccontext.enums import Era, Network
from pccontext.models import (
    OfflineTransferGeneral,
    OfflineTransferProtocol,
    OfflineTransferHistory,
    OfflineTransferFile,
    OfflineTransferTransaction,
    OfflineTransfer,
    ProtocolParameters,
    AddressInfo,
    TokenMetadata,
)
from pccontext.models.offline_transfer_model import TransactionJSON


def test_offline_transfer_general(fake_offline_transfer_general):
    # Act
    offline_transfer_general = OfflineTransferGeneral.from_json(
        fake_offline_transfer_general
    )

    # Assert
    assert offline_transfer_general is not None
    assert (
        offline_transfer_general.offline_cli_version
        == fake_offline_transfer_general["offline_cli_version"]
    )
    assert (
        offline_transfer_general.online_cli_version
        == fake_offline_transfer_general["online_cli_version"]
    )
    assert (
        offline_transfer_general.online_node_version
        == fake_offline_transfer_general["online_node_version"]
    )


def test_offline_transfer_protocol(fake_offline_transfer_protocol):
    # Act
    offline_transfer_protocol = OfflineTransferProtocol.from_json(
        fake_offline_transfer_protocol
    )

    # Assert
    assert offline_transfer_protocol is not None
    assert offline_transfer_protocol.parameters == ProtocolParameters.from_json(
        fake_offline_transfer_protocol["parameters"]
    )
    assert offline_transfer_protocol.era == Era(
        fake_offline_transfer_protocol["era"].lower()
    )
    assert offline_transfer_protocol.network == Network(
        fake_offline_transfer_protocol["network"].lower()
    )


def test_offline_transfer_history(fake_offline_transfer_history):
    # Act
    offline_transfer_history = OfflineTransferHistory.from_json(
        fake_offline_transfer_history
    )

    # Assert
    assert offline_transfer_history is not None
    assert offline_transfer_history.date == fake_offline_transfer_history["date"]
    assert offline_transfer_history.action == fake_offline_transfer_history["action"]


def test_offline_transfer_history_to_json(fake_offline_transfer_history):
    # Act
    offline_transfer_history = OfflineTransferHistory.from_json(
        fake_offline_transfer_history
    )

    json_output = offline_transfer_history.to_json()

    # Assert
    assert json_output is not None
    assert json_output == json.dumps(fake_offline_transfer_history)


def test_offline_transfer_file(fake_offline_transfer_file):
    # Act
    offline_transfer_file = OfflineTransferFile.from_json(fake_offline_transfer_file)

    # Assert
    assert offline_transfer_file is not None
    assert offline_transfer_file.name == fake_offline_transfer_file["name"]
    assert offline_transfer_file.date == fake_offline_transfer_file["date"]
    assert offline_transfer_file.size == fake_offline_transfer_file["size"]
    assert offline_transfer_file.base64 == fake_offline_transfer_file["base64"]


def test_offline_transfer_transaction(fake_offline_transfer_transaction):
    # Act
    offline_transfer_transaction = OfflineTransferTransaction.from_json(
        fake_offline_transfer_transaction
    )

    # Assert
    assert offline_transfer_transaction is not None
    assert (
        offline_transfer_transaction.type == fake_offline_transfer_transaction["type"]
    )
    assert (
        offline_transfer_transaction.date == fake_offline_transfer_transaction["date"]
    )
    assert (
        offline_transfer_transaction.stake_address
        == fake_offline_transfer_transaction["stake_address"]
    )
    assert (
        offline_transfer_transaction.from_address
        == fake_offline_transfer_transaction["from_address"]
    )
    assert (
        offline_transfer_transaction.from_name
        == fake_offline_transfer_transaction["from_name"]
    )
    assert (
        offline_transfer_transaction.to_address
        == fake_offline_transfer_transaction["to_address"]
    )
    assert (
        offline_transfer_transaction.to_name
        == fake_offline_transfer_transaction["to_name"]
    )
    assert offline_transfer_transaction.tx_json == TransactionJSON.from_dict(
        fake_offline_transfer_transaction["tx_json"]
    )


def test_offline_transfer(fake_offline_transfer):
    # Act
    offline_transfer = OfflineTransfer.from_json(fake_offline_transfer)

    # Assert
    assert offline_transfer is not None
    assert (
        offline_transfer.general.offline_cli_version
        == fake_offline_transfer["general"]["offline_cli_version"]
    )
    assert (
        offline_transfer.general.online_cli_version
        == fake_offline_transfer["general"]["online_cli_version"]
    )
    assert (
        offline_transfer.general.online_node_version
        == fake_offline_transfer["general"]["online_node_version"]
    )

    assert offline_transfer.protocol.era == Era(
        fake_offline_transfer["protocol"]["era"].lower()
    )
    assert offline_transfer.protocol.network == Network(
        fake_offline_transfer["protocol"]["network"].lower()
    )
    assert offline_transfer.protocol.parameters == ProtocolParameters.from_json(
        fake_offline_transfer["protocol"]["parameters"]
    )
    assert offline_transfer.history == [
        OfflineTransferHistory.from_json(fake_offline_transfer["history"])
    ]
    assert offline_transfer.files == [
        OfflineTransferFile.from_json(fake_offline_transfer["files"])
    ]
    assert offline_transfer.transactions == [
        OfflineTransferTransaction.from_json(fake_offline_transfer["transactions"])
    ]
    assert offline_transfer.addresses == [
        AddressInfo.from_json(fake_offline_transfer["addresses"])
    ]


def test_offline_transfer_to_json(fake_offline_transfer):
    # Act
    offline_transfer = OfflineTransfer.from_json(fake_offline_transfer)

    json_output = offline_transfer.to_json()

    # Assert
    assert json_output is not None
