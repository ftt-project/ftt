from trade.storage.models.portfolio import Portfolio
from trade.storage.repositories.portfolios_repository import PortfoliosRepository

from pytest import fixture


class TestPortfoliosRepository:
    @fixture
    def subject(self):
        return PortfoliosRepository

    @fixture
    def data(self):
        return {
            "name": "Repository 1"
        }

    def test_get_by_name(self, portfolio, subject):
        found = subject.get_by_name(portfolio.name)
        assert found.id == portfolio.id

    def test_creates_portfolio_and_version(self, data, subject):
        result = subject.create(**data)

        assert type(result) == Portfolio
        Portfolio.delete().execute()

    def test_get_securities_for_latest_version(self, subject, portfolio, weight, security):
        result = subject.get_securities(portfolio)

        assert type(result) == list
        assert result[0] == security
