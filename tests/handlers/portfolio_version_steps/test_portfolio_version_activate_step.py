import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_activate_step import (
    PortfolioVersionActivateStep,
)


class TestPortfolioVersionActivateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionActivateStep

    def test_activates_portfolio_version(self, subject, portfolio_version):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_ok()
        assert result.value.active
