from dataclasses import dataclass


@dataclass(frozen=True)
class QuotePortfolio:
    symbol: str
    enter_price: float = None
    quit_price: float = None
    sell_price: float = None

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __hash__(self):
        return self.symbol.__hash__()

    def __lt__(self, other):
        return self.symbol <= other.symbol

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
