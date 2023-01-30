from datetime import datetime
from typing import List

from ftt.storage import schemas, models
from ftt.storage.value_objects import ValueObjectInterface
from ftt.storage.models.base import Base
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.security import Security
from ftt.storage.models.weight import Weight
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)
from ftt.storage.repositories.repository import Repository


class PortfoliosRepository(Repository):
    @classmethod
    def save(cls, model: Portfolio) -> Portfolio:
        model.updated_at = datetime.now()
        model.save()

        return model

    @classmethod
    def get_by_id(cls, portfolio: schemas.Portfolio) -> schemas.Portfolio | None:
        instance = models.Portfolio.get(models.Portfolio.id == portfolio.id)

        return schemas.Portfolio.from_orm(instance)

    @classmethod
    def get_by_name(cls, name: str) -> Base:
        """
        Deprecated
        """
        return Portfolio.get(Portfolio.name == name)

    @classmethod
    def create(cls, portfolio: schemas.Portfolio) -> schemas.Portfolio:
        """
        Creates a new portfolio in the database.

        Parameters:
        ----------
            portfolio (schemas.Portfolio): Portfolio data

        Returns:
        -------
            schemas.Portfolio: Created portfolio with id
        """
        return cls._create(Portfolio, portfolio.dict())

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
        if not portfolio_version:
            return []
        result = (
            Security.select()
            .join(Weight)
            .join(PortfolioVersion)
            .where(PortfolioVersion.id == portfolio_version.id)
        )
        return list(result)

    @classmethod
    def update(cls, portfolio: schemas.Portfolio) -> schemas.Portfolio:
        instance = models.Portfolio.get(models.Portfolio.id == portfolio.id)
        updated_instance = cls._update(instance, portfolio.dict())

        return schemas.Portfolio.from_orm(updated_instance)

    @classmethod
    def find_by_portfolio_version(
        cls, portfolio_version: schemas.PortfolioVersion
    ) -> schemas.Portfolio:
        portfolio_record = (
            Portfolio.select()
            .join(PortfolioVersion)
            .where(PortfolioVersion.id == portfolio_version.id)
            .get()
        )
        return schemas.Portfolio.from_orm(portfolio_record)
