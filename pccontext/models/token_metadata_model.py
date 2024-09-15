from dataclasses import dataclass
from typing import List, Optional, Union

from pydantic import HttpUrl

from pccontext.models import BaseModel

__all__ = ["AnnotatedSignature", "TokenMetadataProperty", "TokenMetadata"]


@dataclass(frozen=True)
class AnnotatedSignature(BaseModel):
    signature: str
    public_key: str


@dataclass(frozen=True)
class TokenMetadataProperty(BaseModel):
    value: Union[int, str, bytes, HttpUrl]
    sequence_number: int
    signatures: List[AnnotatedSignature]


@dataclass(frozen=True)
class TokenMetadata(BaseModel):
    subject: Optional[str]
    policy: Optional[TokenMetadataProperty]
    name: Optional[TokenMetadataProperty]
    url: Optional[TokenMetadataProperty]
    description: Optional[TokenMetadataProperty]
    logo: Optional[TokenMetadataProperty]
    ticker: Optional[TokenMetadataProperty]
