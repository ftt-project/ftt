import json

from PySide6.QtCore import QRunnable, Slot, Signal, QObject, QThread

from ftt.handlers.portfolio_version_load_handler import PortfolioVersionLoadHandler
from ftt.handlers.security_prices_steps.security_prices_load_step import SecurityPricesLoadStep
from pandas import DataFrame
import pandas as pd
import bt


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class FuncWorker(QRunnable):
    def __init__(self, func, portfolio_version_id):
        super().__init__()
        self.func = func
        self.portfolio_version_id = portfolio_version_id
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        res = self.func(self.portfolio_version_id)
        self.signals.result.emit()


class BacktestingWorker(QObject):
    def __init__(self, portfolio_version_id, queue):
        super().__init__()
        self.portfolio_version_id = portfolio_version_id
        self.queue = queue
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        portfolio_version_result = PortfolioVersionLoadHandler().handle(portfolio_version_id=self.portfolio_version_id)

        prices_result = SecurityPricesLoadStep.process(portfolio_version=portfolio_version_result.value)
        data = prices_result.value.prices
        data["Date"] = prices_result.value.datetime_list
        dataframe = DataFrame.from_dict(prices_result.value.prices)
        dataframe['Date'] = pd.to_datetime(dataframe['Date'])  # only in case of daily interval
        dataframe.set_index("Date", inplace=True)
        s = bt.Strategy('s1', [bt.algos.RunMonthly(),
                               bt.algos.SelectAll(),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
        test = bt.Backtest(s, dataframe)
        res = bt.run(test)
        # k = res.plot()

        self.queue.put(res)
        self.signals.result.emit(1)

