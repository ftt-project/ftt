from dataclasses import dataclass
from decimal import Decimal

from ftt.storage.data_objects import DTOInterface


@dataclass
class PortfolioVersionDTO(DTOInterface):
    value: Decimal = None
    period_start: str = None
    period_end: str = None
    interval: str = None
