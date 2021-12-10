from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ftt.storage.data_objects import DTOInterface


@dataclass
class PortfolioVersionDTO(DTOInterface):
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    interval: Optional[str] = None
    value: Optional[Decimal] = None
