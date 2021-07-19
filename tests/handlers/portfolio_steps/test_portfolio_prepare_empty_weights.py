import pytest

from trade.handlers.portfolio_steps.portfolio_prepare_empty_weights_step import (
    PortfolioPrepareEmptyWeightsStep,
)
from trade.handlers.weights_steps.weights_calculate_step import (
    WeightsCalculateStepResult,
)


class TestPortfolioPrepareEmptyWeightsStep:
    @pytest.fixture
    def subject(self):
        return PortfolioPrepareEmptyWeightsStep

    def test_returns_empty_weights(self, subject):
        result = subject.process(securities=["AAPL", "MSFT"])

        assert result.is_ok()
        assert type(result.value) == WeightsCalculateStepResult
        assert result.value.allocation["AAPL"] == 0
        assert result.value.allocation["MSFT"] == 0
        assert result.value.leftover == 0
