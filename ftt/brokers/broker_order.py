from dataclasses import dataclass
from enum import Enum
from typing import Optional


class OrderAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """
    See https://interactivebrokers.github.io/tws-api/basic_orders.html
    """

    MARKET = "MKT"
    LIMIT = "LMT"


@dataclass(frozen=True)
class BrokerOrder:
    action: OrderAction
    total_quantity: float
    order_type: OrderType
    limit_price: Optional[float] = None
