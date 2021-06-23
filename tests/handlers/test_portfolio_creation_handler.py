import pytest

from trade.handlers.portfolio_creation_handler import PortfolioCreationHandler
from trade.storage.models import Portfolio, PortfolioVersion


class TestPortfolioCreationHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioCreationHandler()

    @pytest.fixture
    def data(self):
        return {
            "name": "Repository 1",
            "amount": 10000,
        }

    def test_creates_portfolio(self, subject, data):
        result = subject.handle(**data)
        assert result.is_ok()
        assert type(result.value) == Portfolio
        assert result.value.id is not None

    def test_creates_portfolio_first_version(self, subject, data):
        result = subject.handle(**data)
        assert result.is_ok()
        assert type(result.value.versions[0]) == PortfolioVersion
        assert result.value.versions[0].id is not None
