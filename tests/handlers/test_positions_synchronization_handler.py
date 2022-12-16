import pytest

from ftt.handlers.positions_synchronization_handler import (
    PositionsSynchronizationHandler,
)
from ftt.storage import schemas
from ftt.storage.models import Order


class TestPositionsSynchronizationHandler:
    @pytest.fixture
    def subject(self):
        return PositionsSynchronizationHandler()

    @pytest.fixture
    def broker_service(self, mocker):
        service = mocker.Mock()
        service.open_positions.return_value = []
        service.place_order.return_value = 1782
        return service

    def test_returns_created_orders(
        self, subject, portfolio_version, weight, broker_service
    ):
        result = subject.handle(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id),
            brokerage_service=broker_service,
        )

        assert result.is_ok()
        assert type(result.value) == list
        assert result.value[0].status == Order.Status.SUBMITTED
        assert result.value[0].desired_size == weight.planned_position
