import pandas as pd
import pytest

from ftt.portfolio_management.dtos import PortfolioAllocationDTO
from ftt.portfolio_management.optimization_strategies import (
    HistoricalOptimizationStrategy,
    OptimizationStrategyResolver,
    RiskParityOptimizationStrategy,
)


class TestHistoricalOptimizationStrategy:
    @pytest.fixture
    def subject(self):
        return HistoricalOptimizationStrategy

    def test_optimize_weights_using_historical_optimization_algorithm(
        self, subject, prices_list_factory
    ):
        result = subject(returns=prices_list_factory()).optimize()

        assert type(result) == PortfolioAllocationDTO
        assert result.weights == {
            "A": 0.2002220674020526,
            "B": 0.20022206743949972,
            "C": 0.2002220674522131,
            "D": 0.20022206745177576,
            "E": 0.19911173025445889,
        }
        assert result.sharpe_ratio == 1.7857686182618002
        assert type(result.cov_matrix) == pd.DataFrame


class TestRiskParityOptimizationStrategy:
    @pytest.fixture
    def subject(self):
        return RiskParityOptimizationStrategy

    def test_optimize_weights_using_risk_parity_optimization_algorithm(
        self, subject, prices_list_factory
    ):
        result = subject(returns=prices_list_factory()).optimize()

        assert type(result) == PortfolioAllocationDTO
        assert result.weights == {
            "A": 0.19999999999863521,
            "B": 0.20000000000029788,
            "C": 0.19999999999954424,
            "D": 0.20000000000179705,
            "E": 0.19999999999972562,
        }
        assert result.sharpe_ratio == 1.7857686182706065
        assert type(result.cov_matrix) == pd.DataFrame


class TestOptimizationStrategyResolver:
    @pytest.fixture
    def subject(self):
        return OptimizationStrategyResolver

    def test_resolve_returns_historical_optimization_strategy(self, subject):
        result = subject.resolve(strategy_name="historical")

        assert result == HistoricalOptimizationStrategy

    def test_resolve_returns_risk_parity_optimization_strategy(self, subject):
        result = subject.resolve(strategy_name="risk_parity")

        assert result == RiskParityOptimizationStrategy
