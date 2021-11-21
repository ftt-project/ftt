from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from ftt.storage.data_objects import DTOInterface


@dataclass
class PortfolioVersionDTO(DTOInterface):
    value: Optional[Decimal] = None
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    interval: Optional[str] = None
