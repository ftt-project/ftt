import pytest

from trade.handlers.portfolio_version_steps.portfolio_version_load_step import PortfolioVersionLoadStep


class TestPortfolioVersionLoadStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionLoadStep

    def test_loads_portfolio_version_by_id(self, subject, portfolio_version):
        result = subject.process(portfolio_version_id=portfolio_version.id)

        assert result.is_ok()
        assert result.value == portfolio_version

    def test_returns_error_when_portfolio_version_is_not_found(self, subject):
        result = subject.process(portfolio_version_id=10)

        assert result.is_err()
        assert result.value == "Portfolio Version with ID 10 does not exist"
