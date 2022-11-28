from datetime import datetime
from typing import Any

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class Security(BaseModel):
    id: int | None
    symbol: str | None = ...

    class Config:
        orm_mode = True


class Portfolio(BaseModel):
    id: int | None
    name: str | None = ...
    value: float | None = ...
    period_start: datetime | None = ...
    period_end: datetime | None = ...
    interval: str | None = ...
    securities: list[Security] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
        fields = {'securities': {'exclude': True}}


class PortfolioSecurity(BaseModel):
    id: int | None
    portfolio: Portfolio = ...
    security: Security = ...

    class Config:
        orm_mode = True
