from PySide6.QtCore import QRunnable, QThreadPool, Slot, Signal, QObject, Qt
import financedatabase as fd

from ftt import models


class WorkerSignals(QObject):
    """
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
    """

    finished = Signal()
    success = Signal(object)
    failed = Signal(object)
    progress = Signal(int)


class TickersLoadWorker(QRunnable):
    def __init__(self):
        super().__init__()

        self.signals = WorkerSignals()

    @classmethod
    def perform(cls):
        threadpool = QThreadPool.globalInstance()
        worker = cls()
        threadpool.start(worker)
        return worker

    @Slot()
    def run(self):
        from PySide6.QtSql import QSqlRelationalTableModel
        from PySide6.QtSql import QSqlTableModel

        db = models.get_db(self.__class__.__name__)
        model = QSqlRelationalTableModel(None, db=db)
        model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        model.setTable("tracking_symbols")

        model.setHeaderData(model.fieldIndex("symbol"), Qt.Horizontal, "Symbol")
        model.setHeaderData(model.fieldIndex("exchange"), Qt.Horizontal, "Exchange")
        model.setHeaderData(model.fieldIndex("currency"), Qt.Horizontal, "Currency")

        all_equities = fd.select_equities()
        # model = models.equity_model_instance()

        for symbol, data in all_equities.items():
            if symbol == '' or symbol is None:
                continue

            models.add_equity(symbol, data['short_name'], data['long_name'], data['summary'], data['currency'], data['sector'], data['industry'], data['exchange'], data['market'], data['country'], data['state'], data['city'], data['zipcode'], data['website'], data['market_cap'],
                              db=db
                              )
            self.signals.progress.emit(1)

        print("done")
        self.signals.success.emit('success')
        self.signals.finished.emit()
