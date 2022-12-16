import pytest

from ftt.handlers.portfolio_version_activation_handler import (
    PortfolioVersionActivationHandler,
)
from ftt.storage import schemas
from tests.helpers import reload_record


class TestPortfolioVersionActivationHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionActivationHandler()

    def test_activates_portfolio_version(
        self, subject, portfolio_version, portfolio, weight
    ):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.handle(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert result.is_ok()
        assert reload_record(portfolio_version).active

    def test_only_one_portfolio_can_be_active(
        self, subject, portfolio_version, portfolio
    ):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.handle(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert result.is_err()
        assert result.unwrap_err() == "Portfolio version #1 is already active"

    def test_process_errors_when_no_weights_associated(
        self, subject, portfolio_version, portfolio
    ):
        portfolio_version.active = False
        portfolio_version.save()

        result = subject.handle(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert result.is_err()
        assert (
            result.unwrap_err()
            == "Portfolio version #1 does not have any weights associated. Run balance step first."
        )

    def test_process_errors_when_weights_planned_positions_is_zero(
        self, subject, portfolio_version, portfolio, weight
    ):
        portfolio_version.active = False
        portfolio_version.save()
        weight.planned_position = 0
        weight.save()

        result = subject.handle(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert result.is_err()
        assert (
            result.unwrap_err()
            == f"Portfolio version #{portfolio_version.id} do not have any planned position greater than 0. Run `portfolio-versions optimize` first."
        )
