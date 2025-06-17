from unittest.mock import MagicMock, patch

from blockfrost import ApiUrls
from pycardano.network import Network as PyCardanoNetwork

from pccontext.enums import Network
from pccontext.backend.blockfrost import BlockFrostChainContext


@patch("pccontext.backend.blockfrost.BlockFrostApi")
def test_blockfrost_chain_context(mock_api):
    mock_api.return_value = MagicMock()
    chain_context = BlockFrostChainContext(
        "project_id", base_url=ApiUrls.mainnet.value, network=Network.MAINNET
    )
    assert chain_context.network == PyCardanoNetwork.MAINNET

    chain_context = BlockFrostChainContext(
        "project_id", base_url=ApiUrls.preprod.value, network=Network.PREPROD
    )
    assert chain_context.network == PyCardanoNetwork.TESTNET

    chain_context = BlockFrostChainContext(
        "project_id", base_url=ApiUrls.preview.value, network=Network.PREVIEW
    )
    assert chain_context.network == PyCardanoNetwork.TESTNET
