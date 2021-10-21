import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_activation_validate_step import (
    PortfolioVersionActivationValidateStep,
)


class TestPortfolioVersionActivationValidateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionActivationValidateStep

    def test_process_returns_ok_when_different_versions(
        self, subject, portfolio, portfolio_version
    ):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_ok()

    def test_process_errors_when_the_same_version(
        self, subject, portfolio, portfolio_version
    ):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_err()
