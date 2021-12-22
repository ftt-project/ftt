import datetime

import pytest
from result import Ok

from ftt.handlers.weights_calculation_handler import WeightsCalculationHandler
from ftt.handlers.weights_steps.weights_calculate_step import WeightsCalculateStepResult
from ftt.storage.models.weight import Weight


class TestWeightsCalculationHandler:
    @pytest.fixture
    def subject(self):
        return WeightsCalculationHandler()

    @pytest.mark.skip(reason="Improve collection to make algorithm run properly or mock")
    def test_calculates_weights_and_persist(
        self, subject, portfolio, portfolio_version, security, security_price, weight, mocker
    ):
        mock = mocker.patch(
            "ftt.handlers.weights_steps.weights_calculate_step.WeightsCalculateStep"
        )
        mock.process.return_value = Ok(WeightsCalculateStepResult(
            allocation=100,
            leftover=20,
            expected_annual_return=0.1,
            annual_volatility=0.2,
            sharpe_ratio=0.3,
        ))
        result = subject.handle(
            portfolio_version=portfolio_version,
            start_period=datetime.date.today() - datetime.timedelta(days=1),
            end_period=datetime.datetime.now(),
            interval='1d',
            persist=True,
        )
        assert result.is_ok()
        assert isinstance(result.value[0], Weight)
        assert result.value[0].portfolio_version == portfolio_version
        assert result.value[0].planned_position == 80
