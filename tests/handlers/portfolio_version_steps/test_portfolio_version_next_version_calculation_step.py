import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_next_version_calculation_step import (
    PortfolioVersionNextVersionCalculationStep,
)
from ftt.storage import schemas


class TestPortfolioVersionNextVersionCalculationStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionNextVersionCalculationStep

    def test_process_returns_next_version_number(
        self, subject, portfolio, portfolio_version
    ):
        schema_portfolio_version = schemas.PortfolioVersion.from_orm(portfolio_version)
        schema_portfolio_version.portfolio = schemas.Portfolio(id=portfolio.id)
        result = subject.process(schema_portfolio_version)

        assert result.is_ok()
        assert isinstance(result.value, int)
        assert result.value > schema_portfolio_version.version

    def test_process_returns_next_version_when_no_versions_exist(
        self, subject, portfolio
    ):
        result = subject.process(portfolio)

        assert result.is_ok()
        assert result.value == 1
