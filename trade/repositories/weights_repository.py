import decimal
from datetime import datetime
from typing import Optional

import peewee

from trade.logger import logger
from trade.models import Base, Weight, Ticker, PortfolioVersion
from trade.repositories.repository_interface import RepositoryInterface


class WeightsRepository(RepositoryInterface):
    @classmethod
    def save(cls, model: Base) -> Base:
        raise NotImplementedError()

    @classmethod
    def upsert(cls, data: dict) -> Base:
        id = (
            Weight.insert(
                portfolio_version=data["portfolio_version"],
                ticker=data["ticker"],
                position=data["position"],
                planned_position=data["planned_position"],
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            .on_conflict(
                conflict_target=(Weight.ticker, Weight.portfolio_version),
                update={Weight.planned_position: data["planned_position"]},
            )
            .execute()
        )

        return cls.get_by_id(id)

    @classmethod
    def find_by_ticker_and_portfolio(
        cls, ticker: Ticker, portfolio_version_id: int
    ) -> Weight:
        return (
            Weight.select()
            .join(PortfolioVersion)
            .switch(Weight)
            .join(Ticker)
            .where(PortfolioVersion.id == portfolio_version_id)
            .where(Ticker.id == ticker.id)
            .get()
        )

    @classmethod
    def update_amount(cls, weight: Weight, amount: float) -> None:
        weight.amount = amount
        weight.save()

    @classmethod
    def create(cls, data: dict) -> Base:
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        return Weight.create(
            portfolio_version=data["portfolio_version"],
            ticker=data["ticker"],
            position=data["position"],
            planned_position=data["planned_position"],
            updated_at=data["updated_at"],
            created_at=data["created_at"],
        )

    @classmethod
    def get_by_id(cls, id: int) -> Base:
        return Weight.get(id)

    @classmethod
    def get_by_ticker_and_portfolio_version(
        cls, ticker_id: int, portfolio_version_id: int
    ) -> Base:
        return (
            Weight.select()
            .join(PortfolioVersion, peewee.JOIN.LEFT_OUTER)
            .switch(Weight)
            .join(Ticker, peewee.JOIN.LEFT_OUTER)
            .where(PortfolioVersion.id == portfolio_version_id)
            .where(Ticker.id == ticker_id)
            .get()
        )

    @classmethod
    def lock_weight(cls, weight: Weight, locked_at_amount: float) -> Weight:
        weight.locked_at = datetime.now()
        weight.locked_at_amount = locked_at_amount
        weight.save()
        return cls.get_by_id(weight.id)

    @classmethod
    def unlock_weight(cls, weight: Weight) -> Weight:
        weight.locked_at = None
        weight.locked_at_amount = None
        weight.save()
        return cls.get_by_id(weight.id)
