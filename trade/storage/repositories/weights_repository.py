from datetime import datetime

import peewee

from trade.storage.models.base import Base
from trade.storage.models.portfolio_version import PortfolioVersion
from trade.storage.models.security import Security
from trade.storage.models.weight import Weight
from trade.storage.repositories.repository_interface import RepositoryInterface


class WeightsRepository(RepositoryInterface):
    @classmethod
    def save(cls, model: Weight) -> Weight:
        raise NotImplementedError()

    @classmethod
    def upsert(cls, data: dict) -> Weight:
        id = (
            Weight.insert(
                portfolio_version=data["portfolio_version"],
                security=data["security"],
                position=data["position"],
                planned_position=data["planned_position"],
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            .on_conflict(
                conflict_target=(Weight.security, Weight.portfolio_version),
                update={Weight.planned_position: data["planned_position"]},
            )
            .execute()
        )

        return cls.get_by_id(id)

    @classmethod
    def find_by_security_and_portfolio(
        cls, security: Security, portfolio_version_id: int
    ) -> Weight:
        return (
            Weight.select()
            .join(PortfolioVersion)
            .switch(Weight)
            .join(Security)
            .where(PortfolioVersion.id == portfolio_version_id)
            .where(Security.id == security.id)
            .get()
        )

    @classmethod
    def update_amount(cls, weight: Weight, amount: float) -> None:
        weight.updated_at = datetime.now()
        weight.amount = amount
        weight.save()

    @classmethod
    def update_on_sell(cls, weight: Weight) -> Weight:
        weight.updated_at = datetime.now()
        weight.amount = 0
        weight.peaked_value = 0
        weight.save()
        return cls.get_by_id(weight.id)

    @classmethod
    def update_on_buy(cls, weight: Weight, amount: float) -> Weight:
        weight.updated_at = datetime.now()
        weight.amount = amount
        weight.save()
        return cls.get_by_id(weight.id)

    @classmethod
    def create(cls, data: dict) -> Weight:
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        return Weight.create(
            portfolio_version=data["portfolio_version"],
            security=data["security"],
            position=data["position"],
            planned_position=data["planned_position"],
            updated_at=data["updated_at"],
            created_at=data["created_at"],
        )

    @classmethod
    def get_by_id(cls, id: int) -> Weight:
        return Weight.get(id)

    @classmethod
    def get_by_security_and_portfolio_version(
        cls, security_id: int, portfolio_version_id: int
    ) -> Base:
        return (
            Weight.select()
            .join(PortfolioVersion, peewee.JOIN.LEFT_OUTER)
            .switch(Weight)
            .join(Security, peewee.JOIN.LEFT_OUTER)
            .where(PortfolioVersion.id == portfolio_version_id)
            .where(Security.id == security_id)
            .get()
        )

    @classmethod
    def lock_weight(cls, weight: Weight, locked_at_amount: float) -> Weight:
        weight.updated_at = datetime.now()
        weight.locked_at = datetime.now()
        weight.locked_at_amount = locked_at_amount
        weight.save()
        return cls.get_by_id(weight.id)

    @classmethod
    def unlock_weight(cls, weight: Weight) -> Weight:
        weight.updated_at = datetime.now()
        weight.locked_at = None
        weight.locked_at_amount = None
        weight.save()
        return cls.get_by_id(weight.id)

    @classmethod
    def update_peaked_value(cls, weight, value):
        weight.updated_at = datetime.now()
        weight.peaked_value = value
        weight.save()
        return cls.get_by_id(weight.id)