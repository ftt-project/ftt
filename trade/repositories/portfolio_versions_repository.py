from datetime import datetime

from trade.models import Base, PortfolioVersion, Portfolio
from trade.repositories.repository_interface import RepositoryInterface


class PortfolioVersionsRepository(RepositoryInterface):
    @classmethod
    def save(cls, model: Base) -> PortfolioVersion:
        raise NotImplementedError()

    @classmethod
    def create(cls, data: dict) -> PortfolioVersion:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        return PortfolioVersion.create(**data)

    @classmethod
    def get_by_id(cls, id: int) -> PortfolioVersion:
        return PortfolioVersion.get(id)

    @classmethod
    def get_by_name(cls, name: str) -> PortfolioVersion:
        raise NotImplementedError()

    @classmethod
    def get_latest_version(cls, portfolio_id: int) -> PortfolioVersion:
        return (
            PortfolioVersion.select()
            .where(PortfolioVersion.portfolio_id == portfolio_id)
            .order_by(PortfolioVersion.version.desc())
            .get()
        )

    @classmethod
    def get_portfolio(cls, portfolio_version_id) -> Portfolio:
        portfolio_versions = PortfolioVersion.get_by_id(portfolio_version_id)
        return portfolio_versions.portfolio
