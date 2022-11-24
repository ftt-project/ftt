from collections import namedtuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QWidget, QVBoxLayout, QLabel, QPushButton, \
    QHBoxLayout

from ftt.ui.model import get_model
from ftt.ui.portfolio.data import getPortfolioVersionWeights
from ftt.ui.portfolio.views.add_securties_dialog import AddSecuritiesDialog
from ftt.ui.state import get_state


class PortfolioVersionWeightsTable(QWidget):
    def __init__(self):
        super().__init__()

        self._buttons = None
        self._layout = None
        self._table = None
        self._model = get_model()
        self._state = get_state()

        self.createUI()

        self._state.signals.selectedPortfolioChanged.connect(
            self.onPortfolioVersionSelected
        )
        self._state.signals.selectedPortfolioVersionChanged.connect(
            self.onPortfolioVersionSelected
        )

    def createUI(self):
        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)

        self._table = QTableWidget()
        self._table.setMinimumHeight(300)
        self._table.setMaximumHeight(500)

        self._table.setColumnCount(4)
        self._table.setHorizontalHeaderLabels(
            ["Security", "Position", "Planned Position", "Amount"]
        )
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.verticalHeader().setVisible(False)

        self._layout.addWidget(
            QLabel("<h4>Securities and Weights</h4>"), 0, alignment=Qt.AlignTop
        )
        self._layout.addWidget(self._table)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)

        self._buttons = namedtuple("Buttons", ["add", "remove"])
        self._buttons.add = QPushButton("Add Security")
        self._buttons.add.setEnabled(False)
        self._buttons.add.clicked.connect(
            lambda: self._state.display_add_security_dialog()
        )
        self._state.signals.selectedPortfolioVersionChanged.connect(
            lambda: self._buttons.add.setEnabled(self._model.portfolio_version_id is not None)
        )
        buttons_layout.addWidget(self._buttons.add)

        self._buttons.remove = QPushButton("Remove Selected")
        self._buttons.remove.setEnabled(False)
        self._buttons.remove.clicked.connect(
            lambda: self._state.display_remove_security_dialog()
        )
        buttons_layout.addWidget(self._buttons.remove)

        self._layout.addLayout(buttons_layout)

        # add_security_dialog = AddSecuritiesDialog()
        # self._state.signals.addSecurityDialogDisplayed.connect(
        #     lambda: add_security_dialog.exec()
        # )

    def onPortfolioVersionSelected(self, portfolio_version_ids):
        print(f"Portfolio version selected: {portfolio_version_ids}")
        self.updateWeights()

    def onPortfolioVersionUnselected(self):
        self.updateWeights()

    def updateWeights(self):
        self._table.clearContents()
        if (
            self._model.portfolio_version_id is None
            or self._model.portfolio_version_id == -1
        ):
            return

        weights = getPortfolioVersionWeights(self._model.portfolio_version_id)
        self._table.setRowCount(len(weights))
        for idx, item in enumerate(weights):
            security = QTableWidgetItem(item.security.symbol)
            position = QTableWidgetItem(f"{item.position}")
            planned_position = QTableWidgetItem(f"{item.planned_position}")
            amount = QTableWidgetItem(f"{item.amount}")

            self._table.setItem(idx, 0, security)
            self._table.setItem(idx, 1, position)
            self._table.setItem(idx, 2, planned_position)
            self._table.setItem(idx, 3, amount)
