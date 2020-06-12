from abc import ABC, abstractmethod


class Basic(ABC):
    @classmethod
    @abstractmethod
    def get_quote(cls, symbol):
        pass

    @classmethod
    @abstractmethod
    def get_quotes(cls, symbols):
        pass
