from datetime import datetime
from typing import List, Optional, Union

from ftt.storage import schemas, models
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.repositories.repository import Repository


class PortfolioVersionsRepository(Repository):
    @classmethod
    def save(
        cls, model: schemas.PortfolioVersion
    ) -> Union[schemas.PortfolioVersion, None]:
        if not model.id:
            raise ValueError("Portfolio version ID is required")

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
        if not portfolio_version.portfolio:
            raise ValueError("Portfolio is required")

        fields = portfolio_version.dict(exclude_unset=True, exclude={"portfolio"})
        fields["portfolio_id"] = portfolio_version.portfolio.id

        record = cls._create(PortfolioVersion, fields)
        return schemas.PortfolioVersion.from_orm(record)

    @classmethod
    def get_by_id(
        cls, portfolio_version: schemas.PortfolioVersion
    ) -> schemas.PortfolioVersion:
        return schemas.PortfolioVersion.from_orm(
            PortfolioVersion.get(portfolio_version.id)
        )

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
        query = (
            PortfolioVersion.select()
            .join(Portfolio)
            .where(Portfolio.id == portfolio.id)
            .where(PortfolioVersion.active == True)  # noqa: E712
        )

        if query.exists():
            return schemas.PortfolioVersion.from_orm(query.get())
        else:
            return None

    @classmethod
    def get_all_by_portfolio(
        cls, portfolio: schemas.Portfolio
    ) -> List[schemas.PortfolioVersion]:
        if not portfolio.id:
            raise ValueError("Portfolio ID is required")

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
        """
        Deprecated
        Use PortfoliosRepository.find_by_portfolio_version instead
        """
        portfolio_versions = PortfolioVersion.get_by_id(portfolio_version_id)
        return portfolio_versions.portfolio

    @classmethod
    def update(
        cls, portfolio_version: schemas.PortfolioVersion
    ) -> schemas.PortfolioVersion:
        if not portfolio_version.id:
            raise ValueError("Portfolio version ID is required")

        fields = portfolio_version.dict(exclude_unset=True)
        record = cls._get_by_id(PortfolioVersion, portfolio_version.id)
        result = cls._update(record, fields)
        return schemas.PortfolioVersion.from_orm(result)

    @classmethod
    def delete(
        cls, portfolio_version: schemas.PortfolioVersion, soft_delete: bool = True
    ) -> bool:
        if not portfolio_version.id:
            raise ValueError("Portfolio version ID is required")

        record = cls._get_by_id(models.PortfolioVersion, portfolio_version.id)
        return cls._delete(record, soft_delete)
