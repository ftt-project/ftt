import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_activation_validate_step import (
    PortfolioVersionActivationValidateStep,
)
from ftt.storage import schemas


class TestPortfolioVersionActivationValidateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionActivationValidateStep

    def test_process_returns_ok_when_different_versions(
        self, subject, portfolio, portfolio_version, weight
    ):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.process(
            portfolio_version=schemas.PortfolioVersion.from_orm(portfolio_version)
        )

        assert result.is_ok()
        assert isinstance(result.value, schemas.PortfolioVersion)

    def test_process_errors_when_the_same_version(
        self, subject, portfolio, portfolio_version, weight
    ):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_err()

    def test_process_errors_when_no_weights(
        self, subject, portfolio, portfolio_version
    ):
        portfolio_version.active = False
        portfolio_version.save()
        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_err()
        assert (
            result.value
            == "Portfolio version #1 does not have any weights associated. Run balance step first."
        )

    def test_process_errors_when_weight_planned_position_is_zero(
        self, subject, portfolio, portfolio_version, weight, security
    ):
        portfolio_version.active = False
        portfolio_version.save()
        weight.planned_position = 0
        weight.save()

        result = subject.process(portfolio_version=portfolio_version)

        assert result.is_err()
        assert (
            result.value
            == f"Portfolio version #{portfolio_version.id} do not have any planned position greater than 0. "
            "Run `portfolio-versions optimize` first."
        )
