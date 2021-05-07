from datetime import datetime

from trade.models import Base, Portfolio, PortfolioVersion
from trade.repositories.portfolio_versions_repository import PortfolioVersionsRepository
from trade.repositories.repository_interface import RepositoryInterface


class PortfoliosRepository(RepositoryInterface):
    def __init__(self, model=Portfolio):
        self.model = model

    def save(self, model: Base):
        raise NotImplementedError()

    def get_by_id(self, id: int):
        return self.model.get(id)

    def get_by_name(self, name: str) -> Base:
        return self.model.get(self.model.name == name)

    def create(self, data: dict) -> Base:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        portfolio = self.model.create(**data)
        PortfolioVersionsRepository().create({
            "version": 1,
            "portfolio": portfolio,
            "updated_at": data["updated_at"],
            "created_at": data["created_at"]
        })
        return portfolio
