import pytest

from ftt.handlers.portfolio_update_handler import PortfolioUpdateHandler


class TestPortfolioUpdateHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioUpdateHandler()

    def test_updates_name(self, subject, portfolio):
        name = "new name"
        result = subject.handle(portfolio=portfolio, params={"name": name})

        assert result.is_ok()
        assert portfolio.name == name
