from datetime import datetime

from trade.models import Base, Weight
from trade.repositories.repository_interface import RepositoryInterface


class WeightsRepository(RepositoryInterface):
    def __init__(self, model=Weight):
        self.model = model

    def save(self, model: Base) -> Base:
        raise NotImplementedError()

    def create(self, data: dict) -> Base:
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        return self.model.create(
            portfolio_version=data['portfolio_version'],
            ticker=data['ticker'],
            position=data['position'],
            planned_position=data['planned_position'],
            updated_at=data["updated_at"],
            created_at=data["created_at"]
        )

    def get_by_id(self, id: int) -> Base:
        raise NotImplementedError()

    def get_by_name(self, name: str) -> Base:
        raise NotImplementedError()
