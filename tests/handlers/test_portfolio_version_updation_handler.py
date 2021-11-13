import pytest

from ftt.handlers.portfolio_version_updation_handler import (
    PortfolioVersionUpdationHandler,
)


class TestPortfolioVersionUpdateHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionUpdationHandler()

    @pytest.fixture
    def params(self):
        return {
            "amount": 110,
            "period_start": "2019-01-01",
            "period_end": "2019-01-31",
            "interval": "1mo",
        }

    def test_updates_portfolio_version(self, subject, portfolio_version, params):
        result = subject.handle(portfolio_version=portfolio_version, params=params)

        assert result.is_ok()
        assert portfolio_version.amount == params["amount"]
        assert portfolio_version.period_start == params["period_start"]
        assert portfolio_version.period_end == params["period_end"]
        assert portfolio_version.interval == params["interval"]
