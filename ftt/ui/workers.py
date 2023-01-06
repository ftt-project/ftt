from typing import Callable, Optional

from PySide6.QtCore import QRunnable, Slot, QThreadPool
from result import Ok, Err, Result

from ftt.handlers.portfolio_version_handlers import PortfolioVersionOptimizationHandler
from ftt.handlers.securities_external_information_loading_handler import (
    SecuritiesExternalInformationLoadingHandler,
)
from ftt.storage import schemas, Storage
from ftt.storage.models import Weight
from ftt.ui.worker_signals import WorkerSignals


class SecuritiesInformationLoadingWorker(QRunnable):
    def __init__(self, securities: list[schemas.Security]):
        super().__init__()
        self.signals = WorkerSignals()
        self.securities = securities

    @classmethod
    def perform(
        cls,
        securities: list[schemas.Security],
        success_callback: Callable = None,
        failure_callback: Callable = None,
        complete_callback: Callable = None,
    ) -> QRunnable:
        threadpool = QThreadPool.globalInstance()
        worker = cls(securities)
        worker.signals.success.connect(success_callback)
        worker.signals.failed.connect(failure_callback)
        worker.signals.finished.connect(complete_callback)
        threadpool.start(worker)
        return worker

    @Slot()
    def run(self):
        result: list[
            schemas.Security
        ] = SecuritiesExternalInformationLoadingHandler().handle(
            securities=self.securities
        )
        match result:
            case Ok(securities):
                self.signals.success.emit(securities)
            case Err(error):
                self.signals.failed.emit(error)
        self.signals.finished.emit()


class PortfolioVersionOptimizationWorker(QRunnable):
    def __init__(self, portfolio_version: schemas.PortfolioVersion):
        super().__init__()
        self.signals = WorkerSignals()
        self.portfolio_version = portfolio_version

    @classmethod
    def perform(
        cls,
        portfolio_version: schemas.PortfolioVersion,
        success_callback: Callable = None,
        failure_callback: Callable = None,
        complete_callback: Callable = None,
    ) -> QRunnable:
        threadpool = QThreadPool.globalInstance()
        worker = cls(portfolio_version=portfolio_version)
        worker.signals.success.connect(success_callback)
        worker.signals.failed.connect(failure_callback)
        worker.signals.finished.connect(complete_callback)
        threadpool.start(worker)
        return worker

    @Slot()
    def run(self):
        db = Storage.get_database()
        db.connect(False)
        try:
            result: Result[
                list[Weight], Optional[str]
            ] = PortfolioVersionOptimizationHandler().handle(
                portfolio_version=self.portfolio_version
            )
            match result:
                case Ok(weights):
                    self.signals.success.emit(weights)
                case Err(error):
                    self.signals.failed.emit(error)
        finally:
            db.close()
            self.signals.finished.emit()
