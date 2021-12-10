import pytest

from ftt.handlers.portfolio_steps.portfolio_prepare_empty_weights_step import (
    PortfolioPrepareEmptyWeightsStep,
)
from ftt.handlers.weights_steps.weights_calculate_step import WeightsCalculateStepResult
from ftt.storage.data_objects.security_dto import SecurityDTO


class TestPortfolioPrepareEmptyWeightsStep:
    @pytest.fixture
    def subject(self):
        return PortfolioPrepareEmptyWeightsStep

    @pytest.fixture
    def security_dtos(self):
        return [SecurityDTO(symbol="AAPL",), SecurityDTO(symbol="MSFT",)]

    def test_returns_empty_weights(self, subject, security_dtos):
        result = subject.process(securities=security_dtos)

        assert result.is_ok()
        assert type(result.value) == WeightsCalculateStepResult
        assert result.value.allocation["AAPL"] == 0
        assert result.value.allocation["MSFT"] == 0
        assert result.value.leftover == 0
