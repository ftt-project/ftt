from dataclasses import dataclass

from ftt.storage.data_objects import DTOInterface


@dataclass
class SecurityDTO(DTOInterface):
    symbol: str
    quote_type: str = None
    sector: str = None
    country: str = None
    industry: str = None
    currency: str = None
    exchange: str = None
    short_name: str = None
    long_name: str = None
