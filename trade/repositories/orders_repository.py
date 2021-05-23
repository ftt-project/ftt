from datetime import datetime
from typing import List

from trade.logger import logger
from trade.models import Base, Order, Portfolio, PortfolioVersion, Ticker
from trade.repositories import TickersRepository, PortfolioVersionsRepository
from trade.repositories.repository_interface import RepositoryInterface


class OrdersRepository(RepositoryInterface):
    @classmethod
    def save(cls, model: Base) -> Order:
        pass

    @classmethod
    def create(cls, data: dict) -> Order:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        return Order.create(**data)

    @classmethod
    def update_status(cls, order_id: int, status: str) -> Order:
        order = cls.get_by_id(order_id)
        order.status = status
        order.updated_at = datetime.now()
        order.save()
        return cls.get_by_id(order_id)

    @classmethod
    def build_and_create(
        cls,
        symbol_name: str,
        portfolio_version_id: int,
        desired_price: float,
        type: str,
    ) -> Order:
        order = cls.create(
            {
                "ticker": TickersRepository().get_by_name(symbol_name),
                "portfolio_version": PortfolioVersionsRepository().get_by_id(
                    portfolio_version_id
                ),
                "desired_price": desired_price,
                "status": Order.Created,
                "type": type,
            }
        )
        return order

    @classmethod
    def get_by_id(cls, id: int) -> Order:
        return Order.get(id)

    @classmethod
    def get_orders_by_portfolio(cls, portfolio: Portfolio) -> List[Order]:
        result = (
            Order.select()
            .join(PortfolioVersion)
            .join(Portfolio)
            .where(Portfolio.id == portfolio.id)
            .execute()
        )
        return list(result)

    @classmethod
    def last_not_closed_order(cls, portfolio: Portfolio, ticker: Ticker) -> Order:
        found = (
            Order.select()
            .join(PortfolioVersion)
            .join(Portfolio)
            .switch(Order)
            .join(Ticker)
            .where(Portfolio.id == portfolio.id)
            .where(Order.status.in_(Order.NOT_CLOSED_STATUSES))
            .where(Ticker.id == ticker.id)
            .order_by(Order.created_at.desc())
            .execute()
        )
        if len(found) > 1:
            logger.warning(f"Found multiple unclosed orders for {portfolio}")

        return found[0] if len(found) > 0 else None