from dataclasses import dataclass
from typing import Optional

from ftt.storage.data_objects import ValueObjectInterface


@dataclass
class WeightValueObject(ValueObjectInterface):
    planned_position: Optional[float] = None
    position: Optional[float] = None
    amount: Optional[float] = None
