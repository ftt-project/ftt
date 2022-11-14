import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_delete_step import (
    PortfolioVersionDeleteStep,
)
from ftt.storage.models import PortfolioVersion, Weight


class TestPortfolioVersionDeleteStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionDeleteStep

    def test_deletes_portfolio_version(self, subject, portfolio_version, weight):
        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_ok()
        assert result.value is True
        assert portfolio_version not in PortfolioVersion.select()
        assert portfolio_version in PortfolioVersion.select_deleted()
        assert weight not in Weight.select()
        assert weight in Weight.select_deleted()

    def test_does_not_delete_active_portfolio_version(self, subject, portfolio_version):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_err()
        assert result.unwrap_err() == "Cannot delete active portfolio version"
