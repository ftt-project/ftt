from datetime import datetime
from typing import List, Optional, Union

import peewee
from result import Err, Result, Ok

from ftt.storage import schemas
from ftt.storage.value_objects import PortfolioVersionValueObject
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.repositories.repository import Repository


class PortfolioVersionsRepository(Repository):
    @classmethod
    def save(
        cls, model: schemas.PortfolioVersion
    ) -> Union[schemas.PortfolioVersion, None]:
        record = cls._get_by_id(PortfolioVersion, model.id)
        fields = model.dict(exclude_unset=True, exclude={"portfolio"})
        fields["updated_at"] = datetime.now()
        updated = record.update(**fields).execute()

        # it always returns 1 because updated_at is always updated
        # there were no cases where it returned 0 so far, but this situation is possible
        if updated == 0:
            return None
        else:
            return model

    @classmethod
    def create(
        cls, portfolio_version: schemas.PortfolioVersion
    ) -> schemas.PortfolioVersion:
        fields = portfolio_version.dict(exclude_unset=True, exclude={"portfolio"})
        fields["portfolio_id"] = portfolio_version.portfolio.id

        record = cls._create(PortfolioVersion, fields)
        return schemas.PortfolioVersion.from_orm(record)

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
        versions = PortfolioVersion.select_all().where(
            PortfolioVersion.portfolio_id == portfolio_id
        )
        if len(versions) == 0:
            return None

        return (
            PortfolioVersion.select_all()
            .where(PortfolioVersion.portfolio_id == portfolio_id)
            .order_by(PortfolioVersion.version.desc())
            .get()
        )

    @classmethod
    def get_active_version(
        cls, portfolio: schemas.Portfolio
    ) -> Optional[schemas.PortfolioVersion]:
        try:
            return (
                PortfolioVersion.select()
                .join(Portfolio)
                .where(Portfolio.id == portfolio.id)
                .where(PortfolioVersion.active == True)  # noqa: E712
                .get()
            )
        except peewee.DoesNotExist:
            return None

    @classmethod
    def get_all_by_portfolio(
        cls, portfolio: schemas.Portfolio
    ) -> List[schemas.PortfolioVersion]:
        from ftt.storage.repositories.portfolios_repository import PortfoliosRepository

        portfolio_model = PortfoliosRepository.get_by_id(portfolio)
        portfolio_version_records = (
            PortfolioVersion.select()
            .join(Portfolio)
            .where(Portfolio.id == portfolio_model.id)
        )
        return [
            schemas.PortfolioVersion.from_orm(model)
            for model in portfolio_version_records
        ]

    @classmethod
    def get_portfolio(cls, portfolio_version_id) -> Portfolio:
        portfolio_versions = PortfolioVersion.get_by_id(portfolio_version_id)
        return portfolio_versions.portfolio

    @classmethod
    def update(
        cls, portfolio_version: PortfolioVersion, dto: PortfolioVersionValueObject
    ) -> PortfolioVersion:
        return cls._update(portfolio_version, dto)

    @classmethod
    def delete(
        cls, portfolio_version: PortfolioVersion, soft_delete: bool = True
    ) -> bool:
        return cls._delete(portfolio_version, soft_delete)
