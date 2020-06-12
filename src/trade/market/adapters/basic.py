from abc import ABC, abstractmethod


class Basic(ABC):
    @classmethod
    @abstractmethod
    def get_quote(cls):
        pass

    @classmethod
    @abstractmethod
    def get_quotes(cls):
        pass
