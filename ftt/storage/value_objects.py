from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


class ValueObjectInterface(ABC):
    pass


@dataclass
class OrderValueObject(ValueObjectInterface):
    status: Optional[str] = None
    execution_size: Optional[float] = None
    execution_price: Optional[float] = None
    executed_at: Optional[datetime] = None


@dataclass
class PortfolioSecurityPricesRangeValueObject(ValueObjectInterface):
    prices: dict[str, list]
    datetime_list: list[datetime]


@dataclass
class PortfolioValueObject(ValueObjectInterface):
    name: str


@dataclass
class PortfolioVersionValueObject(ValueObjectInterface):
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    interval: Optional[str] = None
    value: Optional[Decimal] = None
    optimization_strategy_name: Optional[str] = None


@dataclass
class SecurityValueObject(ValueObjectInterface):
    symbol: str
    quote_type: Optional[str] = None
    sector: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    currency: Optional[str] = None
    exchange: Optional[str] = None
    short_name: Optional[str] = None
    long_name: Optional[str] = None


@dataclass
class WeightValueObject(ValueObjectInterface):
    planned_position: Optional[float] = None
    position: Optional[float] = None
    amount: Optional[float] = None


def is_empty(value_object: ValueObjectInterface) -> bool:
    return all([field is None for field in value_object.__dict__.values()])
