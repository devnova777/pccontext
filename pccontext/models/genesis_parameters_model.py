from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, Union

from pccontext.models import BaseModel

__all__ = ["GenesisParameters"]


@dataclass(frozen=True)
class GenesisParameters(BaseModel):
    """
    Genesis parameters dataclass
    """

    era: Optional[str] = field(default=None, metadata={"aliases": ["era"]})

    active_slots_coefficient: Optional[float] = field(
        default=None,
        metadata={
            "aliases": [
                "active_slots_coefficient",
                "activeSlotsCoeff",
                "activeslotcoeff",
            ]
        },
    )
    alonzo_genesis: Optional[Dict[str, Any]] = field(
        default=None,
        metadata={"aliases": ["alonzo_genesis", "alonzoGenesis", "alonzogenesis"]},
    )
    epoch_length: Optional[int] = field(
        default=None,
        metadata={"aliases": ["epoch_length", "epochLength", "epochlength"]},
    )
    gen_delegs: Optional[Dict[str, Any]] = field(
        default=None,
        metadata={"aliases": ["gen_delegs", "genDelegs"]},
    )
    initial_funds: Optional[Dict[str, Any]] = field(
        default=None,
        metadata={"aliases": ["initial_funds", "initialFunds"]},
    )
    max_kes_evolutions: Optional[int] = field(
        default=None,
        metadata={
            "aliases": ["max_kes_evolutions", "maxKESEvolutions", "maxkesrevolutions"]
        },
    )
    max_lovelace_supply: Optional[int] = field(
        default=None,
        metadata={
            "aliases": ["max_lovelace_supply", "maxLovelaceSupply", "maxlovelacesupply"]
        },
    )
    network_id: Optional[str] = field(
        default=None, metadata={"aliases": ["network_id", "networkId", "networkid"]}
    )
    network_magic: Optional[int] = field(
        default=None,
        metadata={"aliases": ["network_magic", "networkMagic", "networkmagic"]},
    )
    protocol_params: Optional[Dict[str, Any]] = field(
        default=None,
        metadata={"aliases": ["protocol_params", "protocolParams"]},
    )
    security_param: Optional[int] = field(
        default=None,
        metadata={"aliases": ["security_param", "securityParam", "securityparam"]},
    )
    slot_length: Optional[int] = field(
        default=None, metadata={"aliases": ["slot_length", "slotLength", "slotlength"]}
    )
    slots_per_kes_period: Optional[int] = field(
        default=None,
        metadata={
            "aliases": [
                "slots_per_kes_period",
                "slotsPerKESPeriod",
                "slotsperkesperiod",
            ]
        },
    )
    staking: Optional[Dict[str, Any]] = field(
        default=None,
        metadata={"aliases": ["staking"]},
    )
    system_start: Optional[Union[int, datetime]] = field(
        default=None,
        metadata={"aliases": ["system_start", "systemStart", "systemstart"]},
    )
    update_quorum: Optional[int] = field(
        default=None,
        metadata={"aliases": ["update_quorum", "updateQuorum", "updatequorum"]},
    )
