from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    action: str
    total_quantity: int
    order_type: str
    limit_price: float
