import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_load_portfolio_step import (
    PortfolioVersionLoadPortfolioStep,
)


class TestPortfolioVersionLoadPortfolio:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionLoadPortfolioStep

    def test_process_returns_portfolio_by_portfolio_version(
        self, subject, portfolio, portfolio_version
    ):
        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_ok()
        assert result.value == portfolio
