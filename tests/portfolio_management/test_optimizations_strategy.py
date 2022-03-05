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
        assert {k: round(v, 2) for k, v in result.weights.items()} == {
            "A": 0.2,
            "B": 0.2,
            "C": 0.2,
            "D": 0.2,
            "E": 0.2,
        }
        assert round(result.sharpe_ratio, 3) == 1.786
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
        assert {k: round(v, 2) for k, v in result.weights.items()} == {
            "A": 0.2,
            "B": 0.2,
            "C": 0.2,
            "D": 0.2,
            "E": 0.2,
        }
        assert round(result.sharpe_ratio, 3) == 1.786
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
