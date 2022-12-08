import pytest

from ftt.handlers.portfolio_steps.portfolio_deactivate_all_versions_step import (
    PortfolioDeactivateAllVersionsStep,
)
from ftt.storage import schemas
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class TestPortfolioDeactivateAllVersionsStep:
    @pytest.fixture
    def subject(self):
        return PortfolioDeactivateAllVersionsStep

    def test_deactivates_all_versions(self, subject, portfolio, portfolio_version):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.process(schemas.Portfolio.from_orm(portfolio))

        assert result.is_ok()
        assert not result.value[0].active

