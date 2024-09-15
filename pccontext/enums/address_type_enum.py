from enum import Enum

__all__ = ["AddressType"]


class AddressType(Enum):
    """
    Enum class for address type
    """

    PAYMENT = "payment"
    STAKE = "stake"
