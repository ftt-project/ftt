from datetime import datetime

import pandas as pd

from trade.models import Base, Ticker
from trade.repositories.repository_interface import RepositoryInterface


class TickersRepository(RepositoryInterface):
    def __init__(self, model=Ticker):
        self.model = model

    def get_by_name(self, name: str) -> Base:
        return self.model.get(self.model.symbol == name)

    def get_by_id(self, id: int) -> Base:
        return self.model.get_by_id(id)

    def save(self, record: Ticker) -> Base:
        record.updated_at = datetime.now()
        record.save()
        return record

    def upsert(self, data: pd.Series) -> Base:
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        result = self.model.get_or_create(
            symbol=data["symbol"], exchange=data["exchange"], defaults=data.to_dict()
        )
        return result

    def exist(self, name: str) -> int:
        count = self.model.select().where(self.model.symbol == name).count()
        return count > 0

    def create(self, data: dict) -> Base:
        raise NotImplementedError()
