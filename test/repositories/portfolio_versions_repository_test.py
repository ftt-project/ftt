from trade.models import PortfolioVersion
from trade.repositories.portfolio_versions_repository import PortfolioVersionsRepository
from pytest import fixture

from trade.repositories.portfolios_repository import PortfoliosRepository


class TestPortfolioVersionsRepository:
    @fixture
    def subject(self):
        return PortfolioVersionsRepository()

    @fixture
    def portfolio(self):
        return PortfoliosRepository().create({"name": "P1"})

    @fixture
    def portfolio_version(self, subject, portfolio):
        return subject.create({"version": 1, "portfolio": portfolio})

    def test_get_latest_version(self, subject, portfolio):
        found = subject.get_latest_version(portfolio_id=portfolio.id)
        assert type(found) == PortfolioVersion
        assert found.version == 1