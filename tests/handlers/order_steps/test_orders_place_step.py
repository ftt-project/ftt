from datetime import datetime

import pytest

from ftt.handlers.order_steps.orders_place_step import OrdersPlaceStep
from ftt.storage import schemas
from ftt.storage.models import Order


class TestOrdersPlaceStep:
    @pytest.fixture
    def subject(self):
        return OrdersPlaceStep

    @pytest.fixture
    def order(self, security, portfolio, portfolio_version, weight):
        return Order.create(
            action=schemas.Order.OrderAction.BUY,
            desired_size=100,
            security=security,
            portfolio=portfolio,
            portfolio_version=portfolio_version,
            weight=weight,
            order_type=schemas.Order.OrderType.MARKET,
            status=schemas.Order.Status.CREATED,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )

    @pytest.fixture
    def broker_service(self, mocker):
        service = mocker.Mock()
        service.place_order.return_value = 1782
        return service

    def test_processes_order_and_returns_internal_id(
        self, order, subject, broker_service
    ):
        result = subject.process([schemas.Order.from_orm(order)], broker_service)

        assert result.is_ok()
        assert isinstance(result.value[0], schemas.Order)
        assert Order.get(order.id).status == schemas.Order.Status.SUBMITTED
        assert Order.get(order.id).external_id == "1782"
