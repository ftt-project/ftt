import matplotlib
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from ftt.ui.backtesting.workers import BacktestingWorker

matplotlib.use('Qt5Agg')


class BacktestingView(QWidget):
    def __init__(self, model):
        super().__init__()

        self._model = model

        self._layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        self._layout.addWidget(self.label)
        self.setLayout(self._layout)

        self.thread = QThread()
        worker = BacktestingWorker(self._model._portfolio_version_ids[0])
        worker.signals.result.connect(self.on_result)
        worker.moveToThread(self.thread)
        worker.run()

    def on_result(self, result):
        k = result.plot()
        sc = FigureCanvasQTAgg(k.get_figure())
        toolbar = NavigationToolbar2QT(sc, self)
        self._layout.addWidget(toolbar)
        self._layout.addWidget(sc)
