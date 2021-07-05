from datetime import datetime

from trade.storage.models.base import Base
from trade.storage.models.portfolio import Portfolio
from trade.storage.models.portfolio_version import PortfolioVersion
from trade.storage.repositories.repository_interface import RepositoryInterface


class PortfolioVersionsRepository(RepositoryInterface):
    @classmethod
    def save(cls, model: Base) -> PortfolioVersion:
        raise NotImplementedError()

    @classmethod
    def create(cls, **data: str) -> PortfolioVersion:
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
        """
        TODO: use model instead of ID
        """
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
