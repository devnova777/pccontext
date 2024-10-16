"""
Cardano Network Enum
"""

from enum import Enum

__all__ = ["Network"]


class Network(Enum):
    """
    Enum class for Cardano Network
    """

    MAINNET = "mainnet"
    PREPROD = "preprod"
    PREVIEW = "preview"
    SANCHONET = "sanchonet"
    GUILDNET = "guildnet"
    CUSTOM = "custom"
