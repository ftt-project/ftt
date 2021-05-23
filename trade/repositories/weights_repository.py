import decimal
from datetime import datetime
from typing import Optional

import peewee

from trade.logger import logger
from trade.models import Base, Weight, Ticker, PortfolioVersion
from trade.repositories.repository_interface import RepositoryInterface


class WeightsRepository(RepositoryInterface):
    def __init__(self, model: Optional[Weight] = Weight):
        self.model = model

    def save(self, model: Base) -> Base:
        raise NotImplementedError()

    def upsert(self, data: dict) -> Base:
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

        return self.get_by_id(id)

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

    def create(self, data: dict) -> Base:
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        return self.model.create(
            portfolio_version=data["portfolio_version"],
            ticker=data["ticker"],
            position=data["position"],
            planned_position=data["planned_position"],
            updated_at=data["updated_at"],
            created_at=data["created_at"],
        )

    def get_by_id(self, id: int) -> Base:
        return self.model.get(id)

    def get_by_ticker_and_portfolio_version(
        self, ticker_id: int, portfolio_version_id: int
    ) -> Base:
        return (
            self.model.select()
            .join(PortfolioVersion, peewee.JOIN.LEFT_OUTER)
            .switch(self.model)
            .join(Ticker, peewee.JOIN.LEFT_OUTER)
            .where(PortfolioVersion.id == portfolio_version_id)
            .where(Ticker.id == ticker_id)
            .get()
        )
