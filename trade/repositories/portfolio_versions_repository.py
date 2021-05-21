from datetime import datetime

from trade.models import Base, PortfolioVersion, Portfolio
from trade.repositories.repository_interface import RepositoryInterface


class PortfolioVersionsRepository(RepositoryInterface):
    def __init__(self, model=PortfolioVersion):
        self.model = model

    def save(self, model: Base) -> PortfolioVersion:
        raise NotImplementedError()

    def create(self, data: dict) -> PortfolioVersion:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        return self.model.create(**data)

    def get_by_id(self, id: int) -> PortfolioVersion:
        return self.model.get(id)

    def get_by_name(self, name: str) -> PortfolioVersion:
        raise NotImplementedError()

    def get_latest_version(self, portfolio_id: int) -> PortfolioVersion:
        return (
            self.model.select()
            .where(self.model.portfolio_id == portfolio_id)
            .order_by(self.model.version.desc())
            .get()
        )

    def get_portfolio(self, portfolio_version_id) -> Portfolio:
        portfolio_versions = self.get_by_id(portfolio_version_id)
        return portfolio_versions.portfolio
