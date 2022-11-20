from dataclasses import dataclass

from ftt.storage.data_objects import ValueObjectInterface


@dataclass
class PortfolioValueObject(ValueObjectInterface):
    name: str
