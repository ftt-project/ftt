import pytest

from ftt.handlers.portfolio_version_deactivation_handler import PortfolioVersionDeactivationHandler


class TestPortfolioVersionDeactivationHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionDeactivationHandler()

    def test_deactivates_portfolio_version(self, subject, portfolio_version, portfolio):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.handle(
            portfolio_version=portfolio_version, portfolio=portfolio
        )

        assert result.is_ok()
        assert not portfolio_version.active

    def test_errors_on_deactivated_portfolio_version(self, subject, portfolio_version, portfolio):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.handle(
            portfolio_version=portfolio_version, portfolio=portfolio
        )

        assert result.is_err()
