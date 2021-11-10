from datetime import datetime
from typing import List

import peewee
from playhouse.shortcuts import update_model_from_dict

from ftt.storage.errors import PersistingError
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
    def get_by_id(cls, id: int):
        return Portfolio.get(id)

    @classmethod
    def get_by_name(cls, name: str) -> Base:
        return Portfolio.get(Portfolio.name == name)

    @classmethod
    def create(cls, **data: str) -> Base:
        return cls._create(Portfolio, data)

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

    @classmethod
    def update(cls, portfolio: Portfolio, params: dict) -> Portfolio:
        try:
            params["updated_at"] = datetime.now()
            model = update_model_from_dict(portfolio, params)
            model.save()
        except (AttributeError, peewee.IntegrityError) as e:
            raise PersistingError(portfolio, params, str(e))

        return model