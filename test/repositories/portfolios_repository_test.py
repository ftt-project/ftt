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

    @fixture
    def portfolio(self, data):
        data["updated_at"] = datetime.now()
        data["created_at"] = datetime.now()
        portfolio = Portfolio.create(**data)
        yield portfolio
        portfolio.delete_instance()
        return portfolio

    @fixture
    def ticker(self):
        return Ticker.create(**{
            "symbol": "AA.XX",
            "exchange": "SYD",
            "company_name": "Company AAXX",
            "exchange_name": "SYD",
            "type": "Stock",
            "type_display": "Stock",
            "industry": "Technologie",
            "currency": "USD",
            "updated_at": datetime.now(),
            "created_at": datetime.now()
        })

    @fixture
    def portfolio_version(self, portfolio):
        return PortfolioVersion.create(
            version=1,
            portfolio=portfolio,
            updated_at=datetime.now(),
            created_at=datetime.now()
        )

    @fixture
    def weight(self, ticker, portfolio_version):
        return Weight.create(
            portfolio_version=portfolio_version,
            ticker=ticker,
            planned_position=0,
            position=10,
            updated_at=datetime.now(),
            created_at=datetime.now()
        )

    @fixture(autouse=True)
    def cleanup(self):
        yield
        Weight.delete().execute()
        PortfolioVersion.delete().execute()
        Portfolio.delete().execute()
        Ticker.delete().execute()

    def test_get_by_name(self, portfolio, subject):
        found = subject.get_by_name("Repository 1")
        assert found.id == portfolio.id

    def test_creates_portfolio_and_version(self, data, subject):
        result = subject.create(data)

        assert type(result) == Portfolio
        assert len(result.versions) == 1
        assert type(result.versions[0]) == PortfolioVersion

    def test_get_tickers_for_latest_version(self, subject, portfolio, weight, ticker):
        result = subject.get_tickers(portfolio)

        assert type(result) == list
        assert result[0] == ticker
