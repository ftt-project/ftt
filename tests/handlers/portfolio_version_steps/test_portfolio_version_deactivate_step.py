import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_deactivate_step import (
    PortfolioVersionDeactivateStep,
)


class TestPortfolioVersionDeactivateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionDeactivateStep

    def test_deactivates_portfolio_version(self, subject, portfolio_version):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_ok()
        assert not result.value.active

    def test_process_does_nothing_if_no_active_version(self, subject):
        result = subject.process(portfolio_version=None)

        assert result.is_ok()
