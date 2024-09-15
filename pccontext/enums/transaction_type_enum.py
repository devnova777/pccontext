from enum import Enum

__all__ = ["TransactionType"]


class TransactionType(Enum):
    """
    Enum class for transaction type
    """

    TRANSACTION = "Transaction"
    ASSET_MINTING = "AssetMinting"
    ASSET_BURNING = "AssetBurning"
    WITHDRAWAL = "Withdrawal"
    STAKE_KEY_REGISTRATION = "StakeKeyRegistration"
    STAKE_KEY_DE_REGISTRATION = "StakeKeyDeRegistration"
    DELEGATION_CERT_REGISTRATION = "DelegationCertRegistration"
    POOL_REGISTRATION = "PoolRegistration"
    POOL_RE_REGISTRATION = "PoolReRegistration"
    POOL_RETIREMENT = "PoolRetirement"
