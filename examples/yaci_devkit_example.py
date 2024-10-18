from pccontext import YaciDevkitChainContext


def main():
    """
    Get the protocol parameters from Yaci Store API
    """

    chain_context = YaciDevkitChainContext(api_url="http://localhost:8080")

    print(chain_context.protocol_param)


if __name__ == "__main__":
    main()
