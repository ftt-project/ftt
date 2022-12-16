import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_deactivate_step import (
    PortfolioVersionDeactivateStep,
)
from ftt.storage import schemas


class TestPortfolioVersionDeactivateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionDeactivateStep

    def test_deactivates_portfolio_version(self, subject, portfolio_version):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.process(
            portfolio_version=schemas.PortfolioVersion.from_orm(portfolio_version)
        )

        assert result.is_ok()
        assert not result.value.active

    def test_process_does_nothing_if_no_active_version(self, subject):
        result = subject.process(portfolio_version=schemas.PortfolioVersion(id=999))

        assert result.is_err()
        assert result.value == "Portfolio Version with ID 999 does not exist"
