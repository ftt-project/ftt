from datetime import datetime

from trade.models import Base, Ticker
from trade.repositories.repository_interface import RepositoryInterface


class TickersRepository(RepositoryInterface):
    def __init__(self, model=Ticker):
        self.model = model

    def get_by_name(self, name: str) -> Base:
        return self.model.get(self.model.name == name)

    def get_by_id(self, id: int) -> Base:
        return self.model.get_by_id(id)

    def save(self, record: Ticker) -> Base:
        record.updated_at = datetime.now()
        record.save()
        return record

    def create(self, data: dict) -> Base:
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        return self.model.create(**data)

    def exist(self, name: str) -> int:
        count = self.model.select().where(self.model.name == name).count()
        return count > 0
