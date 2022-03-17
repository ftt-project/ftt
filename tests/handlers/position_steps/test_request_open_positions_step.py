import pytest

from ftt.brokers.contract import Contract
from ftt.brokers.position import Position
from ftt.handlers.position_steps.request_open_positions_step import (
    RequestOpenPositionsStep,
)


class TestRequestOpenPositionsStep:
    @pytest.fixture
    def subject(self):
        return RequestOpenPositionsStep

    @pytest.fixture
    def position(self):
        Position(
            account="account-123",
            contract=Contract(
                symbol="AAPL",
            ),
            position=10.0,
        )

    def test_returns_open_positions(self, subject, mocker, position):
        mocked = mocker.patch(
            "ftt.handlers.position_steps.request_open_positions_step.build_brokerage_service"
        )
        mocked.return_value.open_positions.return_value = [position]

        result = subject.process()

        assert result.is_ok()
        assert result.value == [position]
