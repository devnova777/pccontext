from pccontext import OgmiosChainContext


def main():
    """
    Get the protocol parameters from Ogmios
    """

    chain_context = OgmiosChainContext(host="localhost", port=1337)

    print(chain_context.protocol_param)


if __name__ == "__main__":
    main()
