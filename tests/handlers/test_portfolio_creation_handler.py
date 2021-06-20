import pytest

from trade.handlers import PortfolioCreationHandler
from trade.storage.models import Portfolio, PortfolioVersion


class TestPortfolioCreationHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioCreationHandler

    @pytest.fixture
    def data(self):
        return {
            "portfolio": {
                "name": "Repository 1",
                "amount": 10000,
            },
            "portfolio_version": {
                "version": 1
            }
        }

    def test_creates_portfolio(self, subject, data):
        result = subject.handle(**data)
        assert result.is_ok()
        assert type(result.value["portfolio"]["result"]) == Portfolio
        assert result.value["portfolio"]["result"].id is not None

    def test_creates_portfolio_first_version(self, subject, data):
        result = subject.handle(**data)
        assert result.is_ok
        assert type(result.value["portfolio_version"]["result"]) == PortfolioVersion
        assert result.value["portfolio_version"]["result"] == result.value["portfolio"]["result"].versions[0]
        assert result.value["portfolio_version"]["result"].id is not None
