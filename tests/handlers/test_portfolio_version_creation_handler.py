import pytest

from ftt.handlers.portfolio_version_creation_handler import (
    PortfolioVersionCreationHandler,
)
from ftt.storage.models import PortfolioVersion


class TestPortfolioVersionCreateHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionCreationHandler()

    def test_creates_new_version(self, subject, portfolio):
        result = subject.handle(
            portfolio=portfolio,
            amount=999,
            period_start="2019-01-01",
            period_end="2019-10-01",
            interval="1mo",
        )

        assert result.is_ok()
        assert type(result.value) == PortfolioVersion
        assert result.value.portfolio == portfolio
        assert result.value.amount == 999
        assert result.value.period_start == "2019-01-01"
        assert result.value.period_end == "2019-10-01"
        assert result.value.interval == "1mo"
