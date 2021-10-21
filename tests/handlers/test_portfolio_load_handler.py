import pytest

from ftt.handlers.portfolio_load_handler import PortfolioLoadHandler


class TestPortfolioLoadHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioLoadHandler()

    def test_loads_portfolio_by_id(self, subject, portfolio):
        result = subject.handle(portfolio_id=portfolio.id)

        assert result.value == portfolio
