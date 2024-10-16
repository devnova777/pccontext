from pycardano import Network

from pccontext import OfflineTransferFileContext


def test_offline_chain_context(offline_transfer_file):
    chain_context = OfflineTransferFileContext(
        offline_transfer_file=offline_transfer_file
    )
    assert isinstance(chain_context.network, Network)
