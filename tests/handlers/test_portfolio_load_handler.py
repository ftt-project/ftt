import pytest

from ftt.handlers.portfolio_load_handler import PortfolioLoadHandler
from ftt.storage import schemas


class TestPortfolioLoadHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioLoadHandler()

    def test_loads_portfolio_by_id(self, subject, portfolio):
        result = subject.handle(portfolio=schemas.Portfolio(id=portfolio.id))

        assert result.value.id == portfolio.id
