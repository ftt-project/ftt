import pytest

from ftt.handlers.portfolio_version_updation_handler import (
    PortfolioVersionUpdationHandler,
)
from ftt.storage.value_objects import PortfolioVersionValueObject


class TestPortfolioVersionUpdateHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionUpdationHandler()

    @pytest.fixture
    def dto(self):
        return PortfolioVersionValueObject(
            value=110,
            period_start="2019-01-01",
            period_end="2019-01-31",
            interval="1mo",
        )

    def test_updates_portfolio_version(self, subject, portfolio_version, dto):
        result = subject.handle(portfolio_version=portfolio_version, dto=dto)

        assert result.is_ok()
        assert portfolio_version.value == dto.value
        assert portfolio_version.period_start == dto.period_start
        assert portfolio_version.period_end == dto.period_end
        assert portfolio_version.interval == dto.interval
