from dataclasses import dataclass
from typing import Optional

from ftt.storage.data_objects import DTOInterface


@dataclass
class WeightDTO(DTOInterface):
    planned_position: Optional[float] = None
    position: Optional[float] = None
    amount: Optional[float] = None
