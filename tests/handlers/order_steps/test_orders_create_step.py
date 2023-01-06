import pytest

from ftt.handlers.order_steps.orders_create_step import OrdersCreateStep
from ftt.storage import schemas
from ftt.storage.models import Order


class TestOrdersCreateStep:
    @pytest.fixture
    def subject(self):
        return OrdersCreateStep

    @pytest.fixture
    def security_1(self, security_factory):
        return security_factory(symbol="AAPL")

    @pytest.fixture
    def security_2(self, security_factory):
        return security_factory(symbol="MSFT")

    @pytest.fixture
    def calculated_position_differences(self, security_1, security_2):
        return [
            schemas.CalculatedPositionDifference(
                symbol=security_1.symbol,
                actual_position_difference=schemas.CalculatedPositionDifference.Difference.BIGGER,
                planned_position=0,
                actual_position=100,
                delta=100,
            ),
            schemas.CalculatedPositionDifference(
                symbol=security_2.symbol,
                actual_position_difference=schemas.CalculatedPositionDifference.Difference.BIGGER,
                planned_position=0,
                actual_position=75,
                delta=75,
            ),
        ]

    @pytest.fixture
    def weights(self, weight_factory, portfolio_version, security_1, security_2):
        return [
            weight_factory(portfolio_version, security_1, 10, 10),
            weight_factory(portfolio_version, security_2, 10, 10),
        ]

    def test_process_returns_created_order(
        self,
        subject,
        calculated_position_differences,
        weights,
        portfolio,
        portfolio_version,
    ):
        result = subject.process(
            calculated_position_differences, weights, portfolio, portfolio_version
        )

        assert result.is_ok()
        assert type(result.value) == list
        assert type(result.value[0]) == schemas.Order
        assert result.value[0].id is not None
        assert result.value[0].status == Order.Status.CREATED
