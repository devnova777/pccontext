from dataclasses import dataclass, field

from pccontext.models import BaseModel

__all__ = ["StakeAddressInfo"]


@dataclass(frozen=True)
class StakeAddressInfo(BaseModel):
    """
    Stake address info model class
    """

    address: str = field(default_factory=str)
    delegation: str = field(default_factory=str)
    reward_account_balance: int = field(default_factory=int)
