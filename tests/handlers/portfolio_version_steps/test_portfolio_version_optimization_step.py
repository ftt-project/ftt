import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_optimization_step import (
    PortfolioVersionOptimizationStep,
)


class TestPortfolioVersionOptimizationStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionOptimizationStep

    @pytest.mark.skip(reason="Not implemented yet")
    def test_process_returns_result(self):
        pass
