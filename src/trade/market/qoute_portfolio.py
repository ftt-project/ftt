from dataclasses import dataclass

@dataclass
class QoutePortfolio:
    symbol: str
    enter_price: float = None
    quit_price: float = None
    sell_price: float = None
