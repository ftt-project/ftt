from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass(frozen=True)
class Order:
    action: str
    total_quantity: float
    order_type: Optional[str] = None
    limit_price: Optional[float] = None

    class Action(str, Enum):
        BUY = "BUY"
        SELL = "SELL"
