from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from fractions import Fraction
from typing import Any, Dict, Optional, Union

from pycardano import GenesisParameters as PyCardanoGenesisParameters

from pccontext.models import BaseModel

__all__ = ["GenesisParameters"]


@dataclass(frozen=True)
class GenesisParameters(BaseModel, PyCardanoGenesisParameters):
    """
    Genesis parameters dataclass
    """

    alonzo_genesis: Optional[Dict[str, Any]] = field(
        default=None,
        metadata={"aliases": ["alonzo_genesis", "alonzoGenesis", "alonzogenesis"]},
    )
    byron_genesis: Optional[Dict[str, Any]] = field(
        default=None,
        metadata={"aliases": ["byron_genesis", "byronGenesis", "byrongenesis"]},
    )
    conway_genesis: Optional[Dict[str, Any]] = field(
        default=None,
        metadata={"aliases": ["conway_genesis", "conwayGenesis", "conwaygenesis"]},
    )
    shelley_genesis: Optional[Dict[str, Any]] = field(
        default=None,
        metadata={"aliases": ["shelley_genesis", "shelleyGenesis", "shelleygenesis"]},
    )

    era: Optional[str] = field(default=None, metadata={"aliases": ["era"]})

    active_slots_coefficient: Optional[Union[Fraction, float]] = field(
        default=None,
        metadata={
            "aliases": [
                "active_slots_coefficient",
                "activeSlotsCoeff",
                "activeslotcoeff",
            ]
        },
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

    def to_pycardano(self) -> PyCardanoGenesisParameters:
        """
        Convert GenesisParameters to PyCardanoGenesisParameters
        :return: PyCardanoGenesisParameters
        """
        return PyCardanoGenesisParameters(
            active_slots_coefficient=(
                Fraction(self.active_slots_coefficient)
                if self.active_slots_coefficient
                else None
            ),
            epoch_length=self.epoch_length,
            max_kes_evolutions=self.max_kes_evolutions,
            max_lovelace_supply=self.max_lovelace_supply,
            network_magic=self.network_magic,
            security_param=self.security_param,
            slot_length=self.slot_length,
            slots_per_kes_period=self.slots_per_kes_period,
            system_start=(
                int(self.system_start.timestamp())
                if isinstance(self.system_start, datetime)
                else self.system_start
            ),
            update_quorum=self.update_quorum,
        )
