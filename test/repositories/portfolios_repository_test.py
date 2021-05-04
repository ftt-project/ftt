from datetime import datetime

from trade.models import Portfolio, PortfolioVersion
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

    @fixture(autouse=True)
    def cleanup(self):
        yield
        PortfolioVersion.delete().execute()
        Portfolio.delete().execute()

    def test_get_by_name(self, portfolio, subject):
        found = subject.get_by_name("Repository 1")
        assert found.id == portfolio.id

    def test_creates_portfolio_and_version(self, data, subject):
        result = subject.create(data)

        assert type(result) == Portfolio
        assert len(result.versions) == 1
        assert type(result.versions[0]) == PortfolioVersion

