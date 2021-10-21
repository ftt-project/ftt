from datetime import datetime
from typing import List

from ftt.logger import logger
from ftt.storage.models.base import Base
from ftt.storage.models.order import Order
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.security import Security
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)
from ftt.storage.repositories.repository_interface import RepositoryInterface
from ftt.storage.repositories.securities_repository import SecuritiesRepository


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
                "security": SecuritiesRepository().get_by_name(symbol_name),
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
    def last_not_closed_order(cls, portfolio: Portfolio, security: Security) -> Order:
        found = (
            Order.select()
            .join(PortfolioVersion)
            .join(Portfolio)
            .switch(Order)
            .join(Security)
            .where(Portfolio.id == portfolio.id)
            .where(Order.status.in_(Order.NOT_CLOSED_STATUSES))
            .where(Security.id == security.id)
            .order_by(Order.created_at.desc())
            .execute()
        )
        if len(found) > 1:
            logger.warning(f"Found multiple unclosed orders for {portfolio}")

        return found[0] if len(found) > 0 else None

    @classmethod
    def last_successful_order(
        cls, portfolio: Portfolio, security: Security, type: str
    ) -> Order:
        found = (
            Order.select()
            .join(PortfolioVersion)
            .join(Portfolio)
            .switch(Order)
            .join(Security)
            .where(Portfolio.id == portfolio.id)
            .where(Order.status.in_(Order.SUCCEED_STATUSES))
            .where(Security.id == security.id)
            .where(Order.type == type)
            .order_by(Order.created_at.desc())
            .limit(1)
            .execute()
        )

        return found[0] if len(found) > 0 else None

    @classmethod
    def set_execution_params(
        cls,
        order: Order,
        execution_size: int,
        execution_price: float,
        execution_value: float,
        execution_commission: float,
    ) -> Order:
        order.execution_size = execution_size
        order.execution_price = execution_price
        order.execution_value = execution_value
        order.execution_commission = execution_commission
        order.executed_at = datetime.now()
        order.save()
        return cls.get_by_id(order.id)
