import datetime

import pytest

from ftt.handlers.backtrading_steps.backtrading_run_step import BacktradingRunStep
from ftt.storage.data_objects.backtesting_result_dto import BacktestingResultDTO


class TestBacktradingRunStep:
    @pytest.fixture
    def subject(self):
        return BacktradingRunStep

    def test_process_runs(
        self,
        subject,
        portfolio_version_factory,
        securities_weights_list_factory,
        security_prices_dataframe_factory,
    ):
        portfolio_version = portfolio_version_factory(
            period_start=datetime.datetime(2020, 1, 1),
            period_end=datetime.datetime(2020, 12, 31),
            interval="1d",
        )
        dataframe = security_prices_dataframe_factory(
            portfolio_version=portfolio_version,
            period_start=datetime.datetime(2020, 1, 1),
            period_end=datetime.datetime(2020, 12, 31),
            interval="1d",
        )

        result = subject.process(
            portfolio_version=portfolio_version, security_prices=dataframe
        )

        assert result.is_ok()
        assert type(result.value) is BacktestingResultDTO
        assert result.value.original_value == portfolio_version.value
        assert result.value.final_value == 30000.0
