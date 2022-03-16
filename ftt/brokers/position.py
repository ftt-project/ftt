from dataclasses import dataclass
from decimal import Decimal

from ftt.brokers.contract import Contract


@dataclass(frozen=True, init=True)
class Position:
    account: str
    contract: Contract
    position: Decimal
    avg_cost: float
