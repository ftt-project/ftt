from dataclasses import dataclass


@dataclass(frozen=True)
class Contract:
    symbol: str
    security_type: str
    exchange: str
    currency: str
    local_symbol: str
