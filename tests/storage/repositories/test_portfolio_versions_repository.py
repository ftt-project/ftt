import pytest

from ftt.storage.errors import PersistingError
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
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
        portfolio_version.version = "10011"
        result = subject.save(portfolio_version)

        assert result == portfolio_version
        assert result.version == "10011"

    def test_get_active_version_when_exists(
        self, subject, portfolio, portfolio_version
    ):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.get_active_version(portfolio)

        assert result == portfolio_version

    def test_get_active_version_returns_none(
        self, subject, portfolio, portfolio_version
    ):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.get_active_version(portfolio)

        assert result is None

    def test_update(self, subject, portfolio_version):
        params = {"interval": "1mo"}
        result = subject.update(portfolio_version, params)

        assert result == portfolio_version
        assert PortfolioVersion.get(portfolio_version.id).interval == "1mo"

    def test_update_unknown_fields(self, subject, portfolio_version):
        params = {"unknown": "New name"}
        with pytest.raises(PersistingError) as exc:
            subject.update(portfolio_version, params)

        assert "Failed to persist `PortfolioVersion` with params" in str(exc.value)

    def test_update_missing_field(self, subject, portfolio_version):
        params = {"period_start": ""}
        with pytest.raises(PersistingError) as exc:
            subject.update(portfolio_version=portfolio_version, params=params)

        assert "Failed to persist `PortfolioVersion` with params" in str(exc.value)
        assert "CHECK constraint failed" in str(exc.value)
