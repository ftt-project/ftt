import pytest

from ftt.handlers.portfolio_steps.portfolio_versions_list_step import (
    PortfolioVersionsListStep,
)
from ftt.storage import schemas


class TestPortfolioVersionsListStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionsListStep

    def test_returns_list_of_portfolio_versions(
        self, subject, portfolio, portfolio_version
    ):
        result = subject.process(schemas.Portfolio.from_orm(portfolio))

        assert result.is_ok()
        assert result.value[0].id == portfolio_version.id
