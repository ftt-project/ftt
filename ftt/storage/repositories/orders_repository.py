from datetime import datetime
from typing import List

from ftt.logger import Logger
from ftt.storage.data_objects.order_dto import OrderDTO
from ftt.storage.models.base import Base
from ftt.storage.models.order import Order
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.security import Security
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)
from ftt.storage.repositories.repository import Repository
from ftt.storage.repositories.securities_repository import SecuritiesRepository
from ftt.storage.repositories.weights_repository import WeightsRepository


class OrdersRepository(Repository):
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
    def update(cls, order: Order, dto: OrderDTO) -> Order:
        return cls._update(order, dto)

    @classmethod
    def build_and_create(
        cls,
        symbol_name: str,
        portfolio_version_id: int,
        weight_id: int,
        desired_price: float,
        order_type: str,
        action: str,
    ) -> Order:
        portfolio_version = PortfolioVersionsRepository().get_by_id(
            portfolio_version_id
        )
        weight = WeightsRepository().get_by_id(weight_id)
        order = cls.create(
            {
                "security": SecuritiesRepository().get_by_name(symbol_name),
                "portfolio": portfolio_version.portfolio,
                "portfolio_version": portfolio_version,
                "weight": weight,
                "desired_price": desired_price,
                "status": Order.Status.CREATED,
                "order_type": order_type,
                "action": action,
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
            .where(Order.status.in_(list(Order.NotClosedStatus)))
            .where(Security.id == security.id)
            .order_by(Order.created_at.desc())
            .execute()
        )
        if len(found) > 1:
            Logger.warning(f"Found multiple unclosed orders for {portfolio}")

        return found[0] if len(found) > 0 else None

    @classmethod
    def last_successful_order(
        cls, portfolio: Portfolio, security: Security, action: str
    ) -> Order:
        found = (
            Order.select()
            .join(PortfolioVersion)
            .join(Portfolio)
            .switch(Order)
            .join(Security)
            .where(Portfolio.id == portfolio.id)
            .where(Order.status.in_(list(Order.SucceedStatus)))
            .where(Security.id == security.id)
            .where(Order.action == action)
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
