from datetime import datetime
from typing import List, Optional, Union

import peewee

from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO
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
    def create(cls, **data) -> PortfolioVersion:
        return cls._create(PortfolioVersion, data)

    @classmethod
    def get_by_id(cls, id: int) -> PortfolioVersion:
        return PortfolioVersion.get(id)

    @classmethod
    def get_by_name(cls, name: str) -> PortfolioVersion:
        raise NotImplementedError()

    @classmethod
    def get_latest_version(cls, portfolio_id: int) -> Union[PortfolioVersion, None]:
        """
        TODO: use model instead of ID
        """
        versions = PortfolioVersion.select().where(
            PortfolioVersion.portfolio_id == portfolio_id
        )
        if len(versions) == 0:
            return None

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

    @classmethod
    def update(
        cls, portfolio_version: PortfolioVersion, dto: PortfolioVersionDTO
    ) -> PortfolioVersion:
        return cls._update(portfolio_version, dto)
