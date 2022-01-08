from dataclasses import dataclass
from typing import Optional

from ftt.storage.data_objects import DTOInterface


@dataclass
class SecurityDTO(DTOInterface):
    symbol: str
    quote_type: Optional[str] = None
    sector: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    currency: Optional[str] = None
    exchange: Optional[str] = None
    short_name: Optional[str] = None
    long_name: Optional[str] = None
