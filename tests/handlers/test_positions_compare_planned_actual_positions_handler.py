import pytest

from ftt.brokers.broker_order import OrderAction
from ftt.handlers.positions_compare_planned_actual_positions_handler import (
    PositionsComparePlannedActualPositionsHandler,
)


class TestPositionsComparePlannedActualPositionsHandler:
    @pytest.fixture
    def subject(self):
        return PositionsComparePlannedActualPositionsHandler()

    @pytest.fixture(autouse=True)
    def mock_server_request(self, mocker):
        mocked_open_positions = mocker.patch(
            "ftt.handlers.position_steps.request_open_positions_step.build_brokerage_service"
        )
        mocked_open_positions.return_value.open_positions.return_value = []

    def test_returns_comparison_of_planned_and_actual_positions(
        self, subject, portfolio_version, weight
    ):
        result = subject.handle(portfolio_version_id=portfolio_version.id)

        assert result.is_ok()
        assert type(result.value) == list
        assert len(result.value) == 1
        assert result.value[0][0].action == OrderAction.BUY
        assert result.value[0][0].total_quantity == weight.planned_position
