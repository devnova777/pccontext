from pathlib import Path

from pccontext import CardanoCliChainContext, CardanoCliNetwork


def main():
    """
    Get the protocol parameters from Cardano CLI
    """

    chain_context = CardanoCliChainContext(
        binary=Path("/path/to/cardano-cli"),
        socket=Path("/path/to/node.socket"),
        config_file=Path("/path/to/config.json"),
        network=CardanoCliNetwork.MAINNET,
    )

    print(chain_context.protocol_param)


if __name__ == "__main__":
    main()
