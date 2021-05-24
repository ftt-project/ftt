from datetime import datetime

import pandas as pd

from trade.models import Base, Ticker
from trade.repositories.repository_interface import RepositoryInterface


class TickersRepository(RepositoryInterface):
    @classmethod
    def get_by_name(cls, name: str) -> Base:
        return Ticker.get(Ticker.symbol == name)

    @classmethod
    def get_by_id(cls, id: int) -> Base:
        return Ticker.get_by_id(id)

    @classmethod
    def save(cls, record: Ticker) -> Base:
        record.updated_at = datetime.now()
        record.save()
        return record

    @classmethod
    def upsert(cls, data: pd.Series) -> Base:
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        result = Ticker.get_or_create(
            symbol=data["symbol"], exchange=data["exchange"], defaults=data.to_dict()
        )
        return result

    @classmethod
    def exist(cls, name: str) -> int:
        count = Ticker.select().where(Ticker.symbol == name).count()
        return count > 0

    @classmethod
    def create(cls, data: dict) -> Base:
        raise NotImplementedError()
