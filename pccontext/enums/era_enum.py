from enum import Enum

__all__ = ["Era"]


class Era(Enum):
    """
    Enum class for Cardano Era
    """

    BYRON = "byron"
    SHELLY = "shelley"
    ALLEGRA = "allegra"
    MARY = "mary"
    ALONZO = "alonzo"
    BABBAGE = "babbage"
    CONWAY = "conway"
