import threading
from time import time

from ftt.brokers.ib.ib_config import IBConfig
from ftt.brokers.utils import build_brokerage_service
from ftt.handlers.positions_compare_planned_actual_positions_handler import \
    PositionsComparePlannedActualPositionsHandler
from ftt.ui.worker_signals import WorkerSignals


class RequestPortfolioChangesWorker:
    def __init__(self, portfolio_version_id):
        self.signals = WorkerSignals()
        self.portfolio_version_id = portfolio_version_id
        self.thread = threading.Thread(target=self.__run, daemon=True)

    def run(self):
        self.thread.start()
        return True

    def __run(self):
        brokerage_service = build_brokerage_service("Interactive Brokers", IBConfig)
        brokerage_service.connect()
        print(time())
        result = PositionsComparePlannedActualPositionsHandler().handle(
            portfolio_version_id=self.portfolio_version_id,
            brokerage_service=brokerage_service,
        )
        print(time())
        brokerage_service.disconnect()
        self.signals.result.emit(result)
