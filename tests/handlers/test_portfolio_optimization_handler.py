import datetime

import pandas as pd
import pytest

from ftt.handlers.portfolio_optimization_handler import PortfolioOptimizationHandler
from tests.helpers import reload_record


class TestPortfolioOptimizationHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioOptimizationHandler()

    def test_handle_optimize_weights(
        self,
        subject,
        portfolio,
        portfolio_version_factory,
        securities_weights_list_factory,
    ):
        period_start = datetime.datetime(2020, 1, 1)
        period_end = datetime.datetime(2020, 12, 31)
        date_range = pd.date_range(start=period_start, end=period_end)
        interval = "1d"

        portfolio_version = portfolio_version_factory(
            period_start=period_start,
            period_end=period_end,
            interval=interval,
        )
        weights = securities_weights_list_factory(
            portfolio_version, n=5, interval=interval, date_range=date_range
        )

        result = subject.handle(
            portfolio_version_id=portfolio_version.id,
            optimization_strategy_name="historical",
            allocation_strategy_name="default",
        )

        assert result.is_ok()
        assert reload_record(weights[0]).planned_position != 0
