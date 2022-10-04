from PySide6.QtCore import Slot, QRunnable

from ftt.brokers.ib.ib_config import IBConfig
from ftt.brokers.utils import build_brokerage_service
from ftt.handlers.position_steps.request_open_positions_step import RequestOpenPositionsStep
from ftt.ui.worker_signals import WorkerSignals


class RequestPortfolioChangesWorker(QRunnable):
    def __init__(self, portfolio_version_id):
        super().__init__()
        self.signals = WorkerSignals()
        self.portfolio_version_id = portfolio_version_id

    @Slot()
    def run(self):
        brokerage_service = build_brokerage_service("Interactive Brokers", IBConfig)
        # TODO use context manager
        brokerage_service.connect()
        result = RequestOpenPositionsStep.process(brokerage_service=brokerage_service)
        brokerage_service.disconnect()
        self.signals.finished.emit()
        self.signals.result.emit(result)


