import pytest

from ftt.brokers.contract import Contract
from ftt.brokers.position import Position
from ftt.handlers.position_steps.request_open_positions_step import (
    RequestOpenPositionsStep,
)
from ftt.storage import schemas


class TestRequestOpenPositionsStep:
    @pytest.fixture
    def subject(self):
        return RequestOpenPositionsStep

    @pytest.fixture
    def position(self):
        schemas.Position(
            account="account-123",
            contract=schemas.Contract(
                symbol="AAPL",
            ),
            position=10.0,
        )

    @pytest.fixture
    def broker_service(self, mocker, position):
        service = mocker.Mock()
        service.open_positions.return_value = [position]
        return service

    def test_returns_open_positions(self, subject, position, broker_service):
        result = subject.process(broker_service)

        assert result.is_ok()
        assert result.value == [position]
