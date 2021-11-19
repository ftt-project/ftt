from dataclasses import dataclass

from ftt.storage.data_objects import DTOInterface


@dataclass
class PortfolioDTO(DTOInterface):
    name: str
