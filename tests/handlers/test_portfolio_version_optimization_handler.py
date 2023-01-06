import datetime

import pandas as pd
import pytest

from ftt.handlers.portfolio_version_handlers import PortfolioVersionOptimizationHandler
from ftt.storage import schemas
from tests.helpers import reload_record


class TestPortfolioVersionOptimizationHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionOptimizationHandler()

    def test_handle_optimize_weights(
        self,
        subject,
        portfolio,
        portfolio_version_factory,
        securities_weights_list_factory,
        portfolio_security_factory,
    ):
        period_start = datetime.datetime(2020, 1, 1)
        period_end = datetime.datetime(2020, 12, 31)
        date_range = pd.date_range(start=period_start, end=period_end)
        interval = "1d"

        portfolio.period_start = period_start
        portfolio.period_end = period_end
        portfolio.interval = interval
        portfolio.save()

        portfolio_version = portfolio_version_factory()

        weights = securities_weights_list_factory(
            portfolio_version, n=5, interval=interval, date_range=date_range
        )
        for w in weights:
            portfolio_security_factory(portfolio=portfolio, security=w.security)

        result = subject.handle(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id),
        )

        assert result.is_ok()
        assert reload_record(weights[0]).planned_position == 6
        assert reload_record(weights[1]).planned_position == 6
        assert reload_record(weights[2]).planned_position == 6
        assert reload_record(weights[3]).planned_position == 6
        assert reload_record(weights[4]).planned_position == 6
        assert reload_record(portfolio_version).expected_annual_return == 31.0
        assert round(reload_record(portfolio_version).annual_volatility, 2) == 8.82
        assert round(reload_record(portfolio_version).sharpe_ratio, 2) == 1.79
