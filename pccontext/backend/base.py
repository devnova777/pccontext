"""Defines interfaces for client codes to interact (read/write) with the blockchain."""

from typing import List

from pycardano import ChainContext as BaseChainContext

from pccontext.models import StakeAddressInfo

__all__ = [
    "ChainContext",
]


class ChainContext(BaseChainContext):

    def stake_address_info(self, stake_address: str) -> List[StakeAddressInfo]:
        """Get the stake address information.

        Args:
            stake_address (str): The stake address.

        Returns:
            List[StakeAddressInfo]: The stake address information.
        """
        raise NotImplementedError()
