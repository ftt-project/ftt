import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_load_portfolio_step import (
    PortfolioVersionLoadPortfolioStep,
)
from ftt.storage import schemas


class TestPortfolioVersionLoadPortfolioStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionLoadPortfolioStep

    def test_process_returns_portfolio_by_portfolio_version(
        self, subject, portfolio, portfolio_version
    ):
        result = subject.process(
            portfolio_version=schemas.PortfolioVersion.from_orm(portfolio_version)
        )

        assert result.is_ok()
        assert isinstance(result.value, schemas.Portfolio)
        assert result.value.id == portfolio.id
