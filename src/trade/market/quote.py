from dataclasses import dataclass


@dataclass
class Quote:
    symbol: str
    open: float = None
    high: float = None
    low: float = None
    close: float = None
    volume: int = None
    change: float = None
    change_percent: float = None

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
