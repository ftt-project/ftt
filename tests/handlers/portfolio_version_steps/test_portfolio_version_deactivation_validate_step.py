import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_deactivation_validate_step import (
    PortfolioVersionDeactivationValidateStep,
)


class TestPortfolioVersionDeactivationValidateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionDeactivationValidateStep

    def test_process_returns_ok_when_version_is_active(
        self, subject, portfolio_version, portfolio
    ):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_err()
        assert (
            result.value == f"Portfolio Version #{portfolio_version.id} is not active"
        )

    def test_process_returns_error_when_version_is_not_active(
        self, subject, portfolio_version, portfolio
    ):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_ok()
