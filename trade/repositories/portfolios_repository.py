from datetime import datetime
from typing import List

from trade.models import Base, Portfolio, PortfolioVersion, Ticker, Weight
from trade.repositories.portfolio_versions_repository import PortfolioVersionsRepository
from trade.repositories.repository_interface import RepositoryInterface


class PortfoliosRepository(RepositoryInterface):
    @classmethod
    def save(cls, model: Base):
        raise NotImplementedError()

    @classmethod
    def get_by_id(cls, id: int):
        return Portfolio.get(id)

    @classmethod
    def get_by_name(cls, name: str) -> Base:
        return Portfolio.get(Portfolio.name == name)

    @classmethod
    def create(cls, data: dict) -> Base:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        portfolio = Portfolio.create(**data)
        PortfolioVersionsRepository().create(
            {
                "version": 1,
                "portfolio": portfolio,
                "updated_at": data["updated_at"],
                "created_at": data["created_at"],
            }
        )
        return portfolio

    @classmethod
    def get_tickers(cls, portfolio: Portfolio) -> List[Ticker]:
        portfolio_version = PortfolioVersionsRepository().get_latest_version(
            portfolio.id
        )
        result = (
            Ticker.select()
            .join(Weight)
            .join(PortfolioVersion)
            .where(PortfolioVersion.id == portfolio_version.id)
        )
        return list(result)
