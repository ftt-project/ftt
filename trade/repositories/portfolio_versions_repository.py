from datetime import datetime

from trade.models import Base, PortfolioVersion
from trade.repositories.repository_interface import RepositoryInterface


class PortfolioVersionsRepository(RepositoryInterface):
    def __init__(self, model=PortfolioVersion):
        self.model = PortfolioVersion

    def save(self, model: Base):
        raise NotImplementedError()

    def create(self, data: dict) -> Base:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        return self.model.create(**data)

    def get_by_id(self, id: int):
        raise NotImplementedError()

    def get_by_name(self, name: str):
        raise NotImplementedError()