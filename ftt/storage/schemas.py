from datetime import datetime, date
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


class Portfolio(BaseModel):
    id: int | None
    name: str | None = ...
    value: float | None = ...
    period_start: datetime | date | None = ...
    period_end: datetime | date | None = ...
    interval: str | None = ...
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
