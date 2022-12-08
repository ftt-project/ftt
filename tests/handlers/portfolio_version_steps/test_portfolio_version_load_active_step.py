import pytest

from ftt.handlers.portfolio_version_steps.portfolio_version_load_active_step import (
    PortfolioVersionLoadActiveStep,
)
from ftt.storage import schemas


class TestPortfolioVersionLoadActiveStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionLoadActiveStep

    def test_returns_active_version(self, subject, portfolio, portfolio_version):
        portfolio_version.active = True
        portfolio_version.save()

        result = subject.process(portfolio=schemas.Portfolio.from_orm(portfolio))

        assert result.is_ok()
        assert result.value == portfolio_version
