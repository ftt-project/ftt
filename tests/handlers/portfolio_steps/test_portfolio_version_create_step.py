import pytest

from trade.handlers.portfolio_steps.portfolio_version_create_step import PortfolioVersionCreateStep
from trade.storage.models import PortfolioVersion


class TestPortfolioVersionCreateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionCreateStep

    @pytest.fixture
    def data(self, portfolio):
        return {
            "portfolio": portfolio,
            "version": 1
        }

    def test_process_creates_portfolio_version(self, subject, data):
        result = subject.process(**data)

        assert result.is_ok()
        assert type(result.value) == PortfolioVersion
        assert result.value.id is not None
