from datetime import datetime
from typing import List, Optional

import peewee

from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.repositories.repository import Repository


class PortfolioVersionsRepository(Repository):
    @classmethod
    def save(cls, model: PortfolioVersion) -> PortfolioVersion:
        model.updated_at = datetime.now()
        model.save()

        return model

    @classmethod
    def create(cls, **data: str) -> PortfolioVersion:
        return cls._create(PortfolioVersion, data)

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
    def get_active_version(cls, portfolio: Portfolio) -> Optional[PortfolioVersion]:
        try:
            return (
                PortfolioVersion.select()
                .join(Portfolio)
                .where(Portfolio.id == portfolio)
                .where(PortfolioVersion.active == True)  # noqa: E712
                .get()
            )
        except peewee.DoesNotExist:
            return None

    @classmethod
    def get_all_by_portfolio(cls, portfolio: Portfolio) -> List[PortfolioVersion]:
        return list(portfolio.versions)

    @classmethod
    def get_portfolio(cls, portfolio_version_id) -> Portfolio:
        portfolio_versions = PortfolioVersion.get_by_id(portfolio_version_id)
        return portfolio_versions.portfolio