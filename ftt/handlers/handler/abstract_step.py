from abc import ABCMeta, abstractmethod
from typing import Any


class MetaStep(ABCMeta):
    class KeyIsMissing(Exception):
        pass

    def __new__(mcs, name, bases, dct):
        x = super().__new__(mcs, name, bases, dct)
        if x.__name__ != "AbstractStep" and not hasattr(x, "key"):
            raise MetaStep.KeyIsMissing(f"{x} must define `key`")
        return x


class AbstractStep(metaclass=MetaStep):
    @classmethod
    @abstractmethod
    def process(cls, *args: Any):
        pass