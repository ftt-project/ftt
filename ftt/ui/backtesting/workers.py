from PySide6.QtCore import Slot, QObject

from ftt.handlers.portfolio_version_load_handler import PortfolioVersionLoadHandler
from ftt.handlers.security_prices_steps.security_prices_load_step import (
    SecurityPricesLoadStep,
)
from pandas import DataFrame
import pandas as pd
import bt  # type: ignore

from ftt.handlers.weights_list_handler import WeightsListHandler
from ftt.ui.worker_signals import WorkerSignals


class BacktestingWorker(QObject):
    def __init__(self, portfolio_version_id):
        super().__init__()
        self.portfolio_version_id = portfolio_version_id
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        portfolio_version_result = PortfolioVersionLoadHandler().handle(
            portfolio_version_id=self.portfolio_version_id
        )

        weights_result = WeightsListHandler().handle(
            portfolio_version=portfolio_version_result.value
        )
        weights_mapping = {
            weight.security.symbol: weight.planned_position
            for weight in weights_result.value
        }
        total_weights = sum(weights_mapping.values())
        weights_mapping = {k: v / total_weights for k, v in weights_mapping.items()}

        prices_result = SecurityPricesLoadStep.process(
            portfolio_version=portfolio_version_result.value
        )
        data = prices_result.value.prices
        data["Date"] = prices_result.value.datetime_list
        dataframe = DataFrame.from_dict(prices_result.value.prices)
        dataframe["Date"] = pd.to_datetime(
            dataframe["Date"]
        )  # only in case of daily interval
        dataframe.set_index("Date", inplace=True)
        s = bt.Strategy(
            "s1",
            [
                bt.algos.RunMonthly(),
                bt.algos.SelectAll(),
                bt.algos.WeighSpecified(**weights_mapping),
                bt.algos.Rebalance(),
            ],
        )
        test = bt.Backtest(s, dataframe)
        res = bt.run(test)

        self.signals.result.emit(res)
