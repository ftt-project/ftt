import pytest

from ftt.handlers.positions_compare_planned_actual_positions_handler import (
    PositionsComparePlannedActualPositionsHandler,
)
from ftt.storage import schemas


class TestPositionsComparePlannedActualPositionsHandler:
    @pytest.fixture
    def subject(self):
        return PositionsComparePlannedActualPositionsHandler()

    @pytest.fixture
    def open_positions(self):
        return []

    def test_returns_comparison_of_planned_and_actual_positions(
        self, subject, portfolio_version, weight, open_positions
    ):
        result = subject.handle(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id),
            open_positions=open_positions,
        )

        assert result.is_ok()
        assert type(result.value) == list
        assert len(result.value) == 1
        assert (
            result.value[0].actual_position_difference
            == schemas.CalculatedPositionDifference.Difference.SMALLER
        )
        assert result.value[0].delta == weight.planned_position
