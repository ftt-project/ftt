from trade.models import PortfolioVersion
from trade.repositories.portfolio_versions_repository import PortfolioVersionsRepository
from pytest import fixture

from trade.repositories.portfolios_repository import PortfoliosRepository


class TestPortfolioVersionsRepository:
    @fixture
    def subject(self):
        return PortfolioVersionsRepository

    def test_get_latest_version(self, subject, portfolio, portfolio_version):
        found = subject.get_latest_version(portfolio_id=portfolio.id)
        assert type(found) == PortfolioVersion
        assert found.version == 1

    def test_get_portfolio(self, subject, portfolio_version, portfolio):
        result = subject.get_portfolio(portfolio_version.id)
        assert result == portfolio
