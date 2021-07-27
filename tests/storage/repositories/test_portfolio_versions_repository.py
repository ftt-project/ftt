from trade.storage.models.portfolio_version import PortfolioVersion
from trade.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)
from pytest import fixture


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

    def test_get_all_by_portfolio(self, subject, portfolio, portfolio_version):
        result = subject.get_all_by_portfolio(portfolio)

        assert type(result) == list
        assert result[0] == portfolio_version

    def test_save(self, subject, portfolio_version):
        portfolio_version.version = '10011'
        result = subject.save(portfolio_version)

        assert result == portfolio_version
        assert result.version == "10011"

    def test_get_active_version_when_exists(self, subject, portfolio, portfolio_version):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.get_active_version(portfolio)

        assert result == portfolio_version

    def test_get_active_version_returns_none(self, subject, portfolio, portfolio_version):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.get_active_version(portfolio)

        assert result is None
