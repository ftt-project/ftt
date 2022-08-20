from dataclasses import dataclass
from typing import Optional

from ftt.storage.data_objects import DTOInterface


@dataclass
class BacktestingResultDTO(DTOInterface):
    original_value: Optional[float] = None
    final_value: Optional[float] = None
