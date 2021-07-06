import pytest

from trade.handlers.portfolio_steps.portfolio_securities_load_step import PortfolioSecuritiesLoadStep


class TestPortfolioSecuritiesLoadStep:
    @pytest.fixture
    def subject(self):
        return PortfolioSecuritiesLoadStep

    def test_loads_securities(self, subject, portfolio, portfolio_version, weight, security):
        result = subject.process(portfolio)

        assert result.is_ok()
        assert len(result.value) == 1
        assert result.value[0] == security

    def test_returns_err_when_no_securities(self, subject, portfolio, portfolio_version):
        result = subject.process(portfolio)

        assert result.is_err()
        assert "No securities in portfolio" in result.value