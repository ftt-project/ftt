from datetime import datetime
from typing import List

from ftt.logger import Logger
from ftt.storage import schemas
from ftt.storage.models.base import Base
from ftt.storage.models.order import Order
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.security import Security
from ftt.storage.repositories.repository import Repository


class OrdersRepository(Repository):
    @classmethod
    def save(cls, model: Base) -> Order:
        raise NotImplementedError()

    @classmethod
    def create(cls, order: schemas.Order) -> schemas.Order:
        fields = order.dict(
            exclude_unset=True,
            exclude={"portfolio_version", "portfolio", "security", "weight"},
        )
        fields["portfolio_id"] = order.portfolio.id
        fields["security_id"] = order.security.id
        fields["weight_id"] = order.weight.id
        fields["portfolio_version_id"] = order.portfolio_version.id
        return schemas.Order.from_orm(cls._create(Order, fields))

    @classmethod
    def update_status(cls, order_id: int, status: str) -> Order:
        order = cls.get_by_id(order_id)
        order.status = status
        order.updated_at = datetime.now()
        order.save()
        return cls.get_by_id(order_id)

    @classmethod
    def update(cls, order: schemas.Order) -> schemas.Order:
        if not order.id:
            raise ValueError("Order ID is required")

        fields = order.dict(exclude_unset=True)
        record = cls._get_by_id(Order, order.id)
        result = cls._update(record, fields)
        return schemas.Order.from_orm(result)

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
