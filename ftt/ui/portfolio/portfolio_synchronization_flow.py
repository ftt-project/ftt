from PySide6.QtCore import Qt, Slot, QThread, QThreadPool
from PySide6.QtWidgets import QProgressDialog

from ftt.handlers.positions_compare_planned_actual_positions_handler import (
    PositionsComparePlannedActualPositionsHandler,
)
from ftt.ui.model import get_model
from ftt.ui.portfolio.views.portfolio_version_synchronization_confirmation_dialog import (
    PortfolioVersionSynchronizationConfirmationDialog,
)
from ftt.ui.portfolio.workers import RequestPortfolioChangesWorker


class PortfolioSynchronizationFlow:
    def __init__(self, parent_view):
        self._progress_dialog = None
        self._model = get_model()
        self._parent_view = parent_view
        self.thread = QThread()
        self.threadpool = QThreadPool.globalInstance()

    def run(self):
        self._progress_dialog = QProgressDialog(
            "Synchronizing...", "Cancel", 0, 0, self._parent_view
        )
        self._progress_dialog.setWindowModality(Qt.ApplicationModal)
        self._progress_dialog.show()
        worker = RequestPortfolioChangesWorker(self._model.currentPortfolioVersionId)

        worker.signals.result.connect(lambda x: self._on_loading_finished(x))
        worker.signals.finished.connect(self._close)
        self.threadpool.start(worker)

    def _close(self):
        self._progress_dialog.close()

    @Slot()
    def _on_loading_finished(self, result):
        result = PositionsComparePlannedActualPositionsHandler().handle(
            portfolio_version_id=self._model.currentPortfolioVersionId,
            open_positions=result.value,
        )
        self._model.currentPortfolioVersionChanges = result.value
        self._progress_dialog.close()

        self._confirmation_dialog = PortfolioVersionSynchronizationConfirmationDialog()
        self._confirmation_dialog.exec()

        self._confirmation_dialog.accepted.connect(self._on_synchronization_confirmed)

    def _on_synchronization_confirmed(self):
        self._progress_dialog.show()

        # 1. take result from PositionsComparePlannedActualPositionsHandler as it is the one confirmed by user
        # 2. using PositionsSynchronizationHandler create local orders
        # 3. in worker sync orders using OrdersPlaceStep
        # 4. send signal that local db is updated to refresh UI

        # result = PositionsSynchronizationHandler().handle(
        #     portfolio_version_id=self._model.currentPortfolioVersionId
        # )
