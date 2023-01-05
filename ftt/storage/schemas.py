from datetime import datetime, date
from enum import Enum
from typing import Any

import peewee
from pydantic import BaseModel, Field
from pydantic.utils import GetterDict


ACCEPTABLE_INTERVALS = [
    "1m",
    "2m",
    "5m",
    "15m",
    "30m",
    "60m",
    "90m",
    "1h",
    "1d",
    "5d",
    "1wk",
    "1mo",
    "3mo",
]


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class Security(BaseModel):
    id: int | None
    symbol: str | None = Field(..., max_length=10)
    quote_type: str | None
    sector: str | None
    country: str | None
    industry: str | None
    currency: str | None = Field(max_length=3)
    exchange: str | None = Field(max_length=10)
    short_name: str | None
    long_name: str | None

    class Config:
        orm_mode = True


class SecurityPrice(BaseModel):
    symbol: str
    security: Security | None
    datetime: datetime | None
    interval: str | None
    open: float | None
    high: float | None
    low: float | None
    close: float | None
    volume: int | None
    change: float | None
    percent_change: float | None

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class Portfolio(BaseModel):
    id: int | None
    name: str | None
    value: float | None
    period_start: datetime | date | None
    period_end: datetime | date | None
    interval: str | None
    securities: list[Security] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
        fields = {"securities": {"exclude": True}}


class PortfolioSecurity(BaseModel):
    id: int | None
    portfolio: Portfolio = ...
    security: Security = ...

    class Config:
        orm_mode = True


class PortfolioVersion(BaseModel):
    id: int | None
    portfolio: Portfolio | None
    version: int | None
    active: bool | None
    optimization_strategy_name: str | None
    allocation_strategy_name: str | None
    expected_annual_return: float | None
    annual_volatility: float | None
    sharpe_ratio: float | None

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

    def __hash__(self):
        return hash(
            (
                type(self),
                self.id,
            )
        )

    def __eq__(self, other):
        return False if other is None else self.id == other.id


class Weight(BaseModel):
    """
    Entity for Weight
    """

    id: int | None
    portfolio_version: PortfolioVersion | None
    security: Security | None
    position: float | None
    planned_position: float | None
    amount: float | None

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class WeightedSecurity(BaseModel):
    """
    Value object for Security that could be weighted
    for a given portfolio and its version
    """

    symbol: str | None
    portfolio: Portfolio | None
    portfolio_version: PortfolioVersion | None
    security: Security | None
    position: float | None
    planned_position: float | None
    amount: float | None
    weighted: bool | None
    discarded: bool | None

    def __hash__(self):
        return hash((type(self),) + (self.symbol, self.portfolio.id))

    def __eq__(self, other):
        return self.symbol == other.symbol and self.portfolio.id == other.portfolio.id

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class Order(BaseModel):
    class Status(str, Enum):
        CREATED = "Created"
        SUBMITTED = "Submitted"
        ACCEPTED = "Accepted"
        PARTIAL = "Partial"
        COMPLETED = "Completed"
        CANCELED = "Canceled"
        EXPIRED = "Expired"
        MARGIN = "Margin"
        REJECTED = "Rejected"

    class OrderAction(str, Enum):
        BUY = "BUY"
        SELL = "SELL"

    class OrderType(str, Enum):
        """
        See https://interactivebrokers.github.io/tws-api/basic_orders.html
        """

        MARKET = "MKT"
        LIMIT = "LMT"

    id: int | None
    action: OrderAction
    order_type: OrderType
    security: Security
    portfolio: Portfolio
    portfolio_version: PortfolioVersion
    weight: Weight
    status: Status
    external_id: str | None
    executed_at: datetime | None
    desired_size: float | None
    desired_price: float | None
    execution_size: int | None
    execution_price: float | None
    execution_value: float | None
    execution_commission: float | None

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class Contract(BaseModel):
    """
    Value object that represents an operation that broker system performs
    """

    symbol: str
    security_type: str | None
    exchange: str | None
    currency: str | None
    local_symbol: str | None


class BrokerOrder(BaseModel):
    action: Order.OrderAction
    total_quantity: float
    order_type: Order.OrderType
    limit_price: float | None


class Position(BaseModel):
    """
    Value object that represents open position in the broker system
    """

    account: str
    contract: Contract | None
    position: float
    avg_cost: float | None = 0.0


class CalculatedPositionDifference(BaseModel):
    """
    Value object that represents a position operation that was calculated
    and is a difference between actual and planned positions on a given security
    """

    class Difference(str, Enum):
        """
        See https://interactivebrokers.github.io/tws-api/basic_orders.html
        """

        BIGGER = "BIGGER"
        SMALLER = "SMALLER"

    symbol: str
    actual_position_difference: Difference
    planned_position: float
    actual_position: float
    delta: float


class SecurityPricesTimeVector(BaseModel):
    """
    Value object that represents a time vector with prices for a given security
    """

    security: Security
    prices: list[float]
    time_vector: list[datetime]