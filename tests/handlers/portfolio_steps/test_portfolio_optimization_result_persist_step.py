import pytest

from ftt.handlers.portfolio_steps.portfolio_optimization_result_persist_step import (
    PortfolioOptimizationResultPersistStep,
)
from ftt.handlers.weights_steps.weights_calculate_step import WeightsCalculateStepResult
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.weight import Weight
from tests.helpers import reload_record


class TestPortfolioOptimizationResultPersistStep:
    @pytest.fixture
    def subject(self):
        return PortfolioOptimizationResultPersistStep

    @pytest.fixture
    def calculation_result(self, security):
        return WeightsCalculateStepResult(
            allocation={security.symbol: 80},
            leftover=25.599999999998545,
            expected_annual_return=10,
            annual_volatility=14,
            sharpe_ratio=15,
        )

    @pytest.fixture
    def optimization_strategy_name(self):
        return "historical"

    def test_persist_weights(
        self, subject, calculation_result, portfolio_version, optimization_strategy_name
    ):
        result = subject.process(
            portfolio_version, calculation_result, optimization_strategy_name
        )

        assert result.is_ok()
        assert type(result.value) == list
        assert isinstance(result.value[0], Weight)

    def test_updates_portfolio_version_with_stats(
        self, subject, calculation_result, portfolio_version, optimization_strategy_name
    ):
        result = subject.process(
            portfolio_version, calculation_result, optimization_strategy_name
        )

        portfolio_version = reload_record(portfolio_version)
        assert result.is_ok()
        assert portfolio_version.expected_annual_return is not None
        assert portfolio_version.annual_volatility is not None
        assert portfolio_version.sharpe_ratio is not None

    def test_updates_portfolio_version_optimization_algorithm(
        self, subject, portfolio_version, calculation_result, optimization_strategy_name
    ):
        assert portfolio_version.optimization_strategy_name is None

        result = subject.process(
            portfolio_version, calculation_result, optimization_strategy_name
        )

        assert result.is_ok()
        assert (
            reload_record(portfolio_version).optimization_strategy_name
            == optimization_strategy_name
        )
