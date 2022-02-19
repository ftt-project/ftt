import pytest

from ftt.handlers.portfolio_steps.portfolio_deletion_validate_step import (
    PortfolioDeletionValidateStep,
)


class TestPortfolioDeletionValidateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioDeletionValidateStep

    def test_process_errors_when_portfolio_version_is_activate(
        self, subject, portfolio, portfolio_version
    ):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.process(portfolio=portfolio)

        assert result.is_err()

    def test_process_succeeds_when_portfolio_version_is_not_activate(
        self, subject, portfolio, portfolio_version
    ):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.process(portfolio=portfolio)

        assert result.is_ok()
