from datetime import datetime

import pytest

from ftt.brokers.broker_order import BrokerOrder
from ftt.handlers.order_steps.place_orders_step import PlaceOrdersStep
from ftt.storage.models import Order


class TestPlaceOrdersStep:
    @pytest.fixture
    def subject(self):
        return PlaceOrdersStep

    @pytest.fixture
    def order(self, security, portfolio, portfolio_version):
        return Order.create(
            action=BrokerOrder.Action.BUY,
            desired_size=100,
            security=security,
            portfolio=portfolio,
            portfolio_version=portfolio_version,
            order_type=BrokerOrder.OrderType.MARKET,
            status=Order.Status.CREATED,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )

    def test_processes_order_and_returns_internal_id(self, order, subject, mocker):
        mocked = mocker.patch(
            "ftt.handlers.order_steps.place_orders_step.build_brokerage_service"
        )
        mocked.return_value.place_order.return_value = 1782

        result = subject.process([order])

        assert result.is_ok()
        assert result.value == [order]
        assert Order.get(order.id).status == Order.Status.SUBMITTED
        assert Order.get(order.id).external_id == '1782'
