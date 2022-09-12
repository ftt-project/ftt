from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStyle, QHBoxLayout, QProgressDialog, QApplication
from result import Ok, Err

from ftt.handlers.positions_synchronization_handler import PositionsSynchronizationHandler


class PortfolioVersionDetailsView(QWidget):
    portfolioAndVersionsChanged = Signal()

    def __init__(self, model):
        super().__init__()
        self._model = model

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.setAlignment(Qt.AlignTop)

        self.setMaximumWidth(400)

        self._createConrols()

    def _createConrols(self):
        self._edit_button = QPushButton("Edit")
        self._rebalance_button = QPushButton("Rebalance")
        self._rebalance_button.clicked.connect(self.onRebalanceClicked)

        self._backtesting_button = QPushButton("Run Backtesting")

        self._active_button = QPushButton("Active")
        self._synch_button = QPushButton("Synchronize with broker")
        self._synch_button.clicked.connect(self.onSynchronizeClicked)
        self._sync_button_help = QPushButton()
        self._sync_button_help.setIcon(self._sync_button_help.style().standardIcon(QStyle.SP_MessageBoxInformation))

        first_row_layout = QHBoxLayout()
        first_row_layout.addWidget(self._rebalance_button)
        first_row_layout.addWidget(self._edit_button)
        first_row_layout.addWidget(self._backtesting_button)
        self._layout.addLayout(first_row_layout)

        second_row_layout = QHBoxLayout()
        second_row_layout.addWidget(self._active_button)
        second_row_layout.addWidget(self._synch_button)
        second_row_layout.addWidget(self._sync_button_help)
        self._layout.addLayout(second_row_layout)

    @Slot(int)
    def onPortfolioChanged(self, portfolio_id):
        self._model.onPortfolioChanged(portfolio_id)

    @Slot(int)
    def onPortfolioVersionChanged(self, portfolio_version_id):
        self._model.onPortfolioVersionChanged(portfolio_version_id)

    @Slot()
    def onRebalanceClicked(self):
        pass

    @Slot()
    def onSynchronizeClicked(self):
        progress = QProgressDialog("Synchronizing with broker system...", "Abort", 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        result = PositionsSynchronizationHandler().handle(
            portfolio_version_id=self._model.getPortfolioVersionId()
        )

        match result:
            case Ok(_):
                self.portfolioAndVersionsChanged.emit()
                progress.hide()
            case Err(e):
                progress.hide()
                raise e