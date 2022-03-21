import pytest

from ftt.handlers.positions_synchronization_handler import (
    PositionsSynchronizationHandler,
)
from ftt.storage.models import Order


class TestPositionsSynchronizationHandler:
    @pytest.fixture
    def subject(self):
        return PositionsSynchronizationHandler()

    @pytest.fixture(autouse=True)
    def mock_server_request(self, mocker):
        mocked_place_orders = mocker.patch(
            "ftt.handlers.order_steps.place_orders_step.build_brokerage_service"
        )
        mocked_place_orders.return_value.place_order.return_value = 1782

        mocked_open_positions = mocker.patch(
            "ftt.handlers.position_steps.request_open_positions_step.build_brokerage_service"
        )
        mocked_open_positions.return_value.open_positions.return_value = []

    def test_returns_created_orders(self, subject, portfolio_version, weight):
        result = subject.handle(portfolio_version_id=portfolio_version.id)

        assert result.is_ok()
        assert type(result.value) == list
        assert result.value[0].status == Order.Status.SUBMITTED
        assert result.value[0].desired_size == weight.planned_position
