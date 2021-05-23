from datetime import datetime

from trade.models import Portfolio, PortfolioVersion, Ticker, Weight
from trade.repositories.portfolios_repository import PortfoliosRepository

from pytest import fixture


class TestPortfoliosRepository:
    @fixture
    def subject(self):
        return PortfoliosRepository()

    @fixture
    def data(self):
        return {
            "name": "Repository 1"
        }

    def test_get_by_name(self, portfolio, subject):
        found = subject.get_by_name(portfolio.name)
        assert found.id == portfolio.id

    def test_creates_portfolio_and_version(self, data, subject):
        result = subject.create(data)

        assert type(result) == Portfolio
        assert len(result.versions) == 1
        assert type(result.versions[0]) == PortfolioVersion

        PortfolioVersion.delete().execute()
        Portfolio.delete().execute()

    def test_get_tickers_for_latest_version(self, subject, portfolio, weight, ticker):
        result = subject.get_tickers(portfolio)

        assert type(result) == list
        assert result[0] == ticker
