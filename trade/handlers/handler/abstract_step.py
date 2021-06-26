from abc import abstractmethod, ABCMeta
from typing import Any


class MetaStep(ABCMeta):
    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        # x.key = None
        return x


class AbstractStep(metaclass=MetaStep):
    @classmethod
    @abstractmethod
    def process(cls, *args: Any):
        pass
