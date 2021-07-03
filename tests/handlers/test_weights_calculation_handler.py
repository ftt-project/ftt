import datetime

import pytest

from trade.handlers.weights_calculation_handler import WeightsCalculationHandler
from trade.storage.models import Weight


class TestWeightsCalculationHandler:
    @pytest.fixture
    def subject(self):
        return WeightsCalculationHandler()

    @pytest.mark.skip(reason="Improve collection to make algorithm run properly")
    def test_calculates_weights_and_persist(self, subject, portfolio, portfolio_version, security, security_price, weight):
        result = subject.handle(
            securities=[security],
            start_period=datetime.date.today() - datetime.timedelta(days=1),
            end_period=datetime.datetime.now(),
            interval="5m",
            portfolio=portfolio,
            portfolio_budget=10000,
            persist=True
        )

        assert result.is_ok()
        assert isinstance(result.value[0], Weight)
        assert result.value[0].portfolio_version == portfolio_version
        assert result.value[0].planned_position == 80
#