import pytest

from ftt.brokers.broker_order import BrokerOrder
from ftt.brokers.contract import Contract
from ftt.handlers.order_steps.create_orders_step import CreateOrdersStep
from ftt.storage.models import Order


class TestCreateOrdersStep:
    @pytest.fixture
    def subject(self):
        return CreateOrdersStep

    @pytest.fixture
    def security_1(self, security_factory):
        return security_factory(symbol="AAPL")

    @pytest.fixture
    def security_2(self, security_factory):
        return security_factory(symbol="MSFT")

    @pytest.fixture
    def order_candidates(self, security_factory, security_1, security_2):
        return [
            (
                BrokerOrder(
                    action=BrokerOrder.Action.SELL,
                    total_quantity=100,
                ),
                Contract(
                    symbol=security_1.symbol,
                ),
            ),
            (
                BrokerOrder(
                    action=BrokerOrder.Action.SELL,
                    total_quantity=75,
                ),
                Contract(
                    symbol=security_2.symbol,
                ),
            ),
        ]

    @pytest.fixture
    def weights(self, weight_factory, portfolio_version, security_1, security_2):
        return [
            weight_factory(portfolio_version, security_1, 10, 10),
            weight_factory(portfolio_version, security_2, 10, 10),
        ]

    def test_process_returns_created_order(
        self, subject, order_candidates, weights, portfolio, portfolio_version
    ):
        result = subject.process(
            order_candidates, weights, portfolio, portfolio_version
        )

        assert result.is_ok()
        assert type(result.value) == list
        assert type(result.value[0]) == Order
        assert result.value[0].id is not None
        assert result.value[0].status == Order.Status.CREATED
