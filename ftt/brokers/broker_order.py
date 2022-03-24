from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass(frozen=True)
class BrokerOrder:
    action: str
    total_quantity: float
    order_type: Optional[str] = None
    limit_price: Optional[float] = None

    class Action(str, Enum):
        BUY = "BUY"
        SELL = "SELL"

    class OrderType(str, Enum):
        """
        See https://interactivebrokers.github.io/tws-api/basic_orders.html
        """

        MARKET = "MKT"
        LIMIT = "LMT"
