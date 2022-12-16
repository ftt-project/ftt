import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)
from ftt.storage import schemas


class TestPortfolioVersionLoadStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionLoadStep

    def test_loads_portfolio_version_by_id(self, subject, portfolio_version):
        result = subject.process(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert result.is_ok()
        assert isinstance(result.value, schemas.PortfolioVersion)
        assert result.value.id == portfolio_version.id

    def test_returns_error_when_portfolio_version_is_not_found(self, subject):
        result = subject.process(portfolio_version=schemas.PortfolioVersion(id=567))

        assert result.is_err()
        assert result.value == "Portfolio Version with ID 567 does not exist"
