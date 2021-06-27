import pytest

from trade.handlers.weights_calculation_handler import WeightsCalculationHandler


class TestWeightsCalculationHandler:
    @pytest.fixture
    def subject(self):
        return WeightsCalculationHandler
