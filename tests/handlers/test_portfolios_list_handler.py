import pytest

from trade.handlers.portfolios_list_handler import PortfoliosListHandler
from trade.storage.models import Portfolio


class TestPortfoliosListHandler:
    @pytest.fixture
    def subject(self):
        return PortfoliosListHandler()

    def test_returns_list_of_portfolio(self, subject, portfolio):
        result = subject.handle()

        assert result.is_ok()
        assert type(result.value[0]) == Portfolio
