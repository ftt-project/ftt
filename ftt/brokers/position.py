from dataclasses import dataclass
from typing import Optional

from ftt.brokers.contract import Contract


@dataclass(frozen=True, init=True)
class Position:
    account: str
    contract: Contract
    position: float
    avg_cost: Optional[float] = 0.0
