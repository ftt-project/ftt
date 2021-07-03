from datetime import datetime
from typing import List

from trade.storage.models import Base, Portfolio, PortfolioVersion, Security, Weight
from trade.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)
from trade.storage.repositories.repository_interface import RepositoryInterface


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
    def create(cls, **data: str) -> Base:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        portfolio = Portfolio.create(**data)

        return portfolio

    @classmethod
    def list(cls) -> List[Portfolio]:
        return Portfolio.select().execute()

    @classmethod
    def get_securities(cls, portfolio: Portfolio) -> List[Security]:
        """
        Deprecate
        """
        portfolio_version = PortfolioVersionsRepository().get_latest_version(
            portfolio.id
        )
        result = (
            Security.select()
            .join(Weight)
            .join(PortfolioVersion)
            .where(PortfolioVersion.id == portfolio_version.id)
        )
        return list(result)
