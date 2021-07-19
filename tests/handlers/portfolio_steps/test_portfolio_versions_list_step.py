import pytest

from trade.handlers.portfolio_steps.portfolio_versions_list_step import (
    PortfolioVersionsListStep,
)


class TestPortfolioVersionsListStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionsListStep

    def test_returns_list_of_portfolio_versions(
        self, subject, portfolio, portfolio_version
    ):
        result = subject.process(portfolio)

        assert result.is_ok()
        assert result.value[0] == portfolio_version
