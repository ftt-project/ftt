import pytest

from trade.handlers.portfolio_version_activation_handler import PortfolioVersionActivationHandler


class TestPortfolioVersionActivationHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionActivationHandler()

    def test_activates_portfolio_version(self, subject, portfolio_version, portfolio):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.handle(portfolio_version=portfolio_version, portfolio=portfolio)

        assert result.is_ok()
        assert portfolio_version.active

    def test_only_one_portfolio_can_be_active(self, subject, portfolio_version, portfolio):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.handle(portfolio_version=portfolio_version, portfolio=portfolio)

        assert result.is_err()
        assert result.err().value == "Portfolio Version #1 is already active"
