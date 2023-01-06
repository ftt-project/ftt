from datetime import datetime

import pytest

from ftt.storage import schemas, models
from ftt.storage.models.order import Order
from ftt.storage.repositories.orders_repository import OrdersRepository


class TestOrdersRepository:
    @pytest.fixture
    def subject(self):
        return OrdersRepository

    def test_create(self, subject, security, portfolio_version, portfolio, weight):
        result = subject.create(
            schemas.Order(
                security=security,
                portfolio=portfolio,
                portfolio_version=portfolio_version,
                weight=weight,
                status=schemas.Order.Status.CREATED,
                order_type=schemas.Order.OrderType.MARKET,
                desired_price=100,
                action=schemas.Order.OrderAction.BUY,
            )
        )

        assert type(result) == schemas.Order
        assert result.id is not None

        models.Order.delete().execute()

    @pytest.mark.skip(reason="Not implemented")
    def test_save(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_get_by_id(self):
        pass

    def test_get_by_portfolio(self, subject, portfolio, order):
        result = subject.get_orders_by_portfolio(portfolio)

        assert type(result) == list
        assert len(result) == 1
        assert result[0] == order

    def test_update_status(self, subject, order):
        result = subject.update_status(status="submitted", order_id=order.id)

        assert result.id == order.id
        assert "submitted" == subject.get_by_id(order.id).status

    def test_last_not_closed_order_when_order_exist(
        self, subject, order, portfolio, portfolio_version, security, weight
    ):
        order_closed = Order.create(
            security=security,
            order_type="BUY",
            action="BUY",
            portfolio=portfolio,
            portfolio_version=portfolio_version,
            weight=weight,
            status=Order.Status.COMPLETED,
            executed_at=datetime.now(),
            desired_price=10,
            execution_price=10,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        found = subject.last_not_closed_order(portfolio, security)
        assert found == order

        order_closed.delete_instance()

    def test_last_not_closed_order_when_no_orders(self, subject, portfolio, security):
        found = subject.last_not_closed_order(portfolio, security)
        assert found is None

    def test_set_execution_params(self, subject, order):
        result = subject.set_execution_params(
            order=order,
            execution_size=1,
            execution_price=100,
            execution_value=200,
            execution_commission=1,
        )
        assert result.execution_size == 1
        assert result.execution_price == 100
        assert result.execution_value == 200
        assert result.execution_commission == 1
        assert result.executed_at is not None

    def test_last_successful_order(self, subject, order, portfolio, security):
        order.status = Order.Status.COMPLETED
        order.save()
        buy_result = subject.last_successful_order(
            portfolio=portfolio, security=security, action="BUY"
        )
        assert order == buy_result

        sell_result = subject.last_successful_order(
            portfolio=portfolio, security=security, action="SELL"
        )
        assert sell_result is None

    def test_update_returns_success(self, subject, order):
        schema_order = schemas.Order(
            id=order.id,
            security=order.security,
            portfolio=order.portfolio,
            portfolio_version=order.portfolio_version,
            weight=order.weight,
            status=schemas.Order.Status(order.status),
            order_type=schemas.Order.OrderType(order.order_type),
            desired_price=order.desired_price,
            action=schemas.Order.OrderAction(order.action),
            desired_size=order.desired_size,
            execution_size=order.execution_size,
            execution_price=order.execution_price,
            execution_value=order.execution_value,
            execution_commission=order.execution_commission,
        )
        schema_order.status = Order.Status.COMPLETED
        schema_order.execution_size = 1

        result = subject.update(schema_order)

        assert result.id == order.id
        assert isinstance(result, schemas.Order)
        assert result.status == Order.Status.COMPLETED
        assert result.execution_size == 1
