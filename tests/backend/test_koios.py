from unittest.mock import patch

from pycardano import Network

from pccontext.backend.koios import KoiosChainContext


def test_koios_chain_context():
    with patch("koios_python.URLs.get_tip"), patch("koios_python.URLs.get_epoch_info"):
        chain_context = KoiosChainContext(api_key="api_key")
    assert chain_context.network == Network.MAINNET
