import pandas as pd
import pytest

from ftt.portfolio_management import PortfolioAllocationDTO
from ftt.portfolio_management.optimization_strategies import (
    HistoricalOptimizationStrategy,
)


class TestHistoricalOptimizationStrategy:
    @pytest.fixture
    def subject(self):
        return HistoricalOptimizationStrategy

    def test_optimize_returns_balanced_portfolio(self, subject, prices_list_factory):
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
