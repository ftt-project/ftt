import pytest

from ftt.handlers.portfolio_version_deletion_handler import (
    PortfolioVersionDeletionHandler,
)
from ftt.storage import schemas
from ftt.storage.models import PortfolioVersion


class TestPortfolioVersionDeletionHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionDeletionHandler()

    def test_deletes_portfolio_version(self, subject, portfolio_version, weight):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.handle(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert result.is_ok()
        assert result.value is True
        assert portfolio_version not in PortfolioVersion.select()

    def test_returns_error_on_portfolio_version_not_found(self, subject):
        result = subject.handle(portfolio_version=schemas.PortfolioVersion(id=999))

        assert result.is_err()
        assert result.unwrap_err() == "Portfolio Version with ID 999 does not exist"

    def test_returns_error_on_active_portfolio_version(
        self, subject, portfolio_version
    ):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.handle(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert result.is_err()
        assert result.unwrap_err() == "Cannot delete active portfolio version"
