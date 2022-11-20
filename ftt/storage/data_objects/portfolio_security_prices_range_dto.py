from dataclasses import dataclass
from datetime import datetime

from ftt.storage.data_objects import ValueObjectInterface


@dataclass
class PortfolioSecurityPricesRangeValueObject(ValueObjectInterface):
    prices: dict[str, list]
    datetime_list: list[datetime]
