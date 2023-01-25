import pytest

from ftt.handlers.securities_handler import PortfolioSecuritiesLoadHandler
from ftt.storage import schemas


class TestPortfolioSecuritiesLoadHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioSecuritiesLoadHandler()

    def test_handle_returns_list_of_securities(
        self, subject, portfolio, security, portfolio_security
    ):
        result = subject.handle(portfolio=schemas.Portfolio(id=portfolio.id))

        assert result.is_ok()
        assert result.value == [security]
