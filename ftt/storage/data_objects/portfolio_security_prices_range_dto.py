from dataclasses import dataclass
from datetime import datetime

from ftt.storage.data_objects import DTOInterface


@dataclass
class PortfolioSecurityPricesRangeDTO(DTOInterface):
    prices: dict[str, list]
    datetime_list: list[datetime]
