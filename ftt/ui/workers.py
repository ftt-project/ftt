from typing import Callable

from PySide6.QtCore import QRunnable, Slot, QThreadPool
from result import Ok, Err

from ftt.handlers.securities_external_information_loading_handler import SecuritiesExternalInformationLoadingHandler
from ftt.storage import schemas
from ftt.ui.worker_signals import WorkerSignals


class SecuritiesInformationLoadingWorker(QRunnable):
    def __init__(self, securities: list[schemas.Security]):
        super().__init__()
        self.signals = WorkerSignals()
        self.securities = securities

    @classmethod
    def perform(cls, securities: list[schemas.Security], success_callback: Callable = None,
                failure_callback: Callable = None, complete_callback: Callable = None) -> QRunnable:
        threadpool = QThreadPool.globalInstance()
        worker = cls(securities)
        worker.signals.success.connect(success_callback)
        worker.signals.failed.connect(failure_callback)
        worker.signals.finished.connect(complete_callback)
        threadpool.start(worker)
        return worker

    @Slot()
    def run(self):
        result: list[schemas.Security] = SecuritiesExternalInformationLoadingHandler().handle(securities=self.securities)
        match result:
            case Ok(securities):
                self.signals.success.emit(securities)
                pass
            case Err(error):
                self.signals.failed.emit(error)
                pass
        self.signals.finished.emit()
