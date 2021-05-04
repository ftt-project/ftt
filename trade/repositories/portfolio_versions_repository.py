from datetime import datetime

from trade.models import Base, PortfolioVersion
from trade.repositories.repository_interface import RepositoryInterface


class PortfolioVersionsRepository(RepositoryInterface):
    def __init__(self, model=PortfolioVersion):
        self.model = PortfolioVersion

    def save(self, model: Base) -> Base:
        raise NotImplementedError()

    def create(self, data: dict) -> Base:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        return self.model.create(**data)

    def get_by_id(self, id: int) -> Base:
        raise NotImplementedError()

    def get_by_name(self, name: str) -> Base:
        raise NotImplementedError()

    def get_latest_version(self, portfolio_id: int) -> Base:
        return (self.model.select()
                .where(self.model.portfolio_id == portfolio_id)
                .order_by(self.model.version.desc())
                .get())
