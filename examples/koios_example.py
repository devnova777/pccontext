import os

from blockfrost import ApiUrls

from pccontext import BlockFrostChainContext, KoiosChainContext


def main():
    """
    Get the protocol parameters from Koios API
    """

    koios_api_key = os.getenv("KOIOS_API_KEY")
    chain_context = KoiosChainContext(api_key=koios_api_key)

    print(chain_context.protocol_param)


if __name__ == "__main__":
    main()
