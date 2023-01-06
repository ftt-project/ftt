import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_optimization_step import (
    PortfolioVersionOptimizationStep,
)
from ftt.storage import schemas


class TestPortfolioVersionOptimizationStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionOptimizationStep

    @pytest.mark.skip(reason="Not implemented yet")
    def test_process_returns_result(self):
        pass

    def test_returns_error_when_prices_are_empty(self, subject, portfolio_version):
        portfolio_version_schema = schemas.PortfolioVersion.from_orm(portfolio_version)
        portfolio_version_schema.optimization_strategy_name = "historical"

        result = subject.process(
            portfolio_version=portfolio_version_schema,
            security_prices=[
                schemas.SecurityPricesTimeVector(
                    security=schemas.Security(symbol="AAPL"),
                    time_vector=[],
                    prices=[],
                )
            ],
        )

        assert result.is_err()
        assert result.unwrap_err() == "Prices for AAPL are empty"
