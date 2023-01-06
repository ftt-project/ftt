import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_deactivation_validate_step import (
    PortfolioVersionDeactivationValidateStep,
)
from ftt.storage import schemas


class TestPortfolioVersionDeactivationValidateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionDeactivationValidateStep

    def test_process_returns_ok_when_version_is_active(
        self, subject, portfolio_version, portfolio
    ):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.process(
            portfolio_version=schemas.PortfolioVersion.from_orm(portfolio_version)
        )

        assert result.is_err()
        assert (
            result.value == f"Portfolio version #{portfolio_version.id} is not active"
        )

    def test_process_returns_error_when_version_is_not_active(
        self, subject, portfolio_version, portfolio
    ):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.process(
            portfolio_version=schemas.PortfolioVersion.from_orm(portfolio_version)
        )

        assert result.is_ok()

    def test_process_returns_error_when_no_such_portfolio_version(
        self, subject, portfolio_version, portfolio
    ):
        result = subject.process(portfolio_version=schemas.PortfolioVersion(id=999))

        assert result.is_err()
        assert result.value == "Portfolio Version with ID 999 does not exist"
