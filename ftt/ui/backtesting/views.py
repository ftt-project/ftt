from queue import Queue

import bt
import matplotlib
import pandas as pd
from PySide6.QtCore import QThreadPool, QThread
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from pandas import DataFrame

from ftt.handlers.security_prices_steps.security_prices_load_step import SecurityPricesLoadStep
from ftt.ui.backtesting.workers import BacktestingWorker, FuncWorker

matplotlib.use('Qt5Agg')

from ftt.handlers.portfolio_version_load_handler import PortfolioVersionLoadHandler


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, fig):
        # fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

        # fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
        # super(MplCanvas, self).__init__(fig)


class BacktestingView(QWidget):
    def __init__(self, model):
        super().__init__()

        self._model = model

        self._layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        self._layout.addWidget(self.label)
        self.setLayout(self._layout)

        self.thread = QThread()
        self.queue = Queue()
        worker = BacktestingWorker(self._model._portfolio_version_ids[0], self.queue)
        worker.signals.result.connect(self.on_result)
        worker.moveToThread(self.thread)
        worker.run()

    def long_running_func(self, portfolio_version_id):
        portfolio_version_result = PortfolioVersionLoadHandler().handle(portfolio_version_id=portfolio_version_id)

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
        return res

    def on_result(self, *args):
        result = self.queue.get()
        k = result.plot()
        sc = FigureCanvasQTAgg(k.get_figure())
        toolbar = NavigationToolbar2QT(sc, self)
        self._layout.addWidget(toolbar)
        self._layout.addWidget(sc)
