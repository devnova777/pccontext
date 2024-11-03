from freezegun import freeze_time
from pycardano import Network

from pccontext import GenesisParameters, OfflineTransferFileContext, ProtocolParameters


def test_offline_chain_context(offline_transfer_file):
    chain_context = OfflineTransferFileContext(
        offline_transfer_file=offline_transfer_file
    )
    assert isinstance(chain_context.network, Network)


def test_protocol_param(offline_transfer_file, cli_protocol_parameters_json):
    chain_context = OfflineTransferFileContext(
        offline_transfer_file=offline_transfer_file
    )
    expected_protocol_params = ProtocolParameters.from_json(
        cli_protocol_parameters_json
    )
    assert chain_context.protocol_param == expected_protocol_params.to_pycardano()


def test_genesis(offline_transfer_file, fake_genesis_parameters_json):
    chain_context = OfflineTransferFileContext(
        offline_transfer_file=offline_transfer_file
    )
    expected_genesis = GenesisParameters.from_json(fake_genesis_parameters_json)
    assert chain_context.genesis_param == expected_genesis.to_pycardano()


@freeze_time("2024-11-2")
def test_epoch(offline_transfer_file):
    chain_context = OfflineTransferFileContext(
        offline_transfer_file=offline_transfer_file
    )
    assert chain_context.epoch == 519
