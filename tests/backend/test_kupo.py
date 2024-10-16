from pycardano import Network

from pccontext import KupoChainContextExtension


def test_kupo_chain_context(ogmios_chain_context):
    chain_context = KupoChainContextExtension(wrapped_backend=ogmios_chain_context)
    assert chain_context.network == Network.TESTNET
