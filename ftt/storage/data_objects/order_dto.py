from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ftt.storage.data_objects import DTOInterface


@dataclass
class OrderDTO(DTOInterface):
    status: Optional[str] = None
    execution_size: Optional[float] = None
    execution_price: Optional[float] = None
    executed_at: Optional[datetime] = None
