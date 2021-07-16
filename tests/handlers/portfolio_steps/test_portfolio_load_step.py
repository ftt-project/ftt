import pytest

from trade.handlers.portfolio_steps.portfolio_load_step import PortfolioLoadStep


class TestPortfolioLoadStep:
    @pytest.fixture
    def subject(self):
        return PortfolioLoadStep

    def test_returns_portfolio_if_it_exists(self, subject, portfolio):
        result = subject.process(portfolio_id=portfolio.id)

        assert result.is_ok()
        assert result.value == portfolio

    def test_returns_error_when_portfolio_does_not_exist(self, subject):
        result = subject.process(portfolio_id=101)

        assert result.is_err()
        assert result.value == "Portfolio with ID 101 does not exist"
