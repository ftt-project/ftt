from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass(frozen=True)
class Contract:
    symbol: str
    security_type: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    local_symbol: Optional[str] = None

    class SecurityType(str, Enum):
        STOCK = "STK"
