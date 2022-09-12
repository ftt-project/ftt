from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QProgressDialog, QStyle, QButtonGroup
from result import Ok, Err

from ftt.handlers.positions_synchronization_handler import PositionsSynchronizationHandler
from ftt.ui.portfolio.models import get_model
from ftt.ui.portfolio.signals import PortfolioSignals


class PortfolioVersionDetailsView(QWidget):
    def __init__(self):
        super().__init__()

        self._model = get_model()
        self.signals = PortfolioSignals()

        self._controls = None
        self._sync_button_help = None
        self._synch_button = None
        self._active_button = None
        self._backtesting_button = None
        self._rebalance_button = None
        self._edit_button = None

        self.createUI()

        self.signals.portfolioVersionSelected.connect(self.onPortfolioVersionChanged)

    def createUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setAlignment(Qt.AlignTop)

        self.setMaximumWidth(400)

        self._controls = QButtonGroup()
        self._controls.setExclusive(False)

        self._edit_button = QPushButton("Edit")
        self._edit_button.setEnabled(False)
        self._controls.addButton(self._edit_button)

        self._rebalance_button = QPushButton("Rebalance")
        self._rebalance_button.setEnabled(False)
        self._controls.addButton(self._rebalance_button)
        self._rebalance_button.clicked.connect(self.onRebalanceClicked)

        self._backtesting_button = QPushButton("Run Backtesting")
        self._backtesting_button.setEnabled(False)
        self._controls.addButton(self._backtesting_button)

        self._active_button = QPushButton("Activate")
        self._active_button.setEnabled(False)
        self._controls.addButton(self._active_button)

        self._synch_button = QPushButton("Synchronize with broker")
        self._synch_button.setEnabled(False)
        self._controls.addButton(self._synch_button)
        self._synch_button.clicked.connect(self.onSynchronizeClicked)

        self._sync_button_help = QPushButton()
        self._sync_button_help.setIcon(self._sync_button_help.style().standardIcon(QStyle.SP_MessageBoxInformation))

        first_row_layout = QHBoxLayout()
        first_row_layout.addWidget(self._rebalance_button)
        first_row_layout.addWidget(self._edit_button)
        first_row_layout.addWidget(self._backtesting_button)
        layout.addLayout(first_row_layout)

        second_row_layout = QHBoxLayout()
        second_row_layout.addWidget(self._active_button)
        second_row_layout.addWidget(self._synch_button)
        second_row_layout.addWidget(self._sync_button_help)
        layout.addLayout(second_row_layout)

    @Slot()
    def onRebalanceClicked(self):
        pass

    @Slot()
    def onSynchronizeClicked(self):
        progress = QProgressDialog("Synchronizing with broker system...", "Abort", 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        result = PositionsSynchronizationHandler().handle(
            portfolio_version_id=self._model.currentPortfolioVersionId
        )

        match result:
            case Ok(_):
                self.signals.portfolioVersionInDBUpdated.emit()
                progress.hide()
            case Err(e):
                progress.hide()
                raise e

    @Slot(int)
    def onPortfolioVersionChanged(self):
        match self._model.currentPortfolioVersionId:
            case -1 | None:
                print("onPortfolioVersionChanged: -1", self._model.currentPortfolioVersionId)
                for button in self._controls.buttons():
                    button.setEnabled(False)
            case _:
                print("onPortfolioVersionChanged: _", self._model.currentPortfolioVersionId)
                for button in self._controls.buttons():
                    button.setEnabled(True)
