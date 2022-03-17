import pytest

from ftt.brokers.contract import Contract
from ftt.brokers.order import Order
from ftt.handlers.order_steps.place_orders_step import PlaceOrdersStep


class TestPlaceOrdersStep:
    @pytest.fixture
    def subject(self):
        return PlaceOrdersStep

    @pytest.fixture
    def order(self):
        return Order(
            action="BUY",
            total_quantity=100.0,
        )

    @pytest.fixture
    def contract(self):
        return Contract(
            symbol="AAPL",
        )

    def test_processes_order_and_returns_internal_id(self, order, contract, subject, mocker):
        mocked = mocker.patch("ftt.handlers.orders.place_orders_step.build_brokerage_service")
        mocked.return_value.place_order.return_value = 1782

        result = subject.process(order, contract)

        assert result.is_ok()
        assert result.value == 1782
