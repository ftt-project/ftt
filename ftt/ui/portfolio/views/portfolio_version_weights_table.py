from PySide6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem

from ftt.ui.model import get_model
from ftt.ui.portfolio.models import getPortfolioVersionWeights
from ftt.ui.state import get_state


class PortfolioVersionWeightsTable(QTableWidget):
    def __init__(self):
        super().__init__()

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
        self.setMinimumHeight(300)
        self.setMaximumHeight(500)

        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(
            ["Security", "Position", "Planned Position", "Amount"]
        )
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.verticalHeader().setVisible(False)

    def onPortfolioVersionSelected(self, portfolio_version_ids):
        print(f"Portfolio version selected: {portfolio_version_ids}")
        self.updateWeights()

    def onPortfolioVersionUnselected(self):
        self.updateWeights()

    def updateWeights(self):
        self.clearContents()
        if (
            self._model.portfolio_version_id is None
            or self._model.portfolio_version_id == -1
        ):
            return
        print(self._model)
        weights = getPortfolioVersionWeights(self._model.portfolio_version_id)
        self.setRowCount(len(weights))
        for idx, item in enumerate(weights):
            security = QTableWidgetItem(item.security.symbol)
            position = QTableWidgetItem(f"{item.position}")
            planned_position = QTableWidgetItem(f"{item.planned_position}")
            amount = QTableWidgetItem(f"{item.amount}")

            self.setItem(idx, 0, security)
            self.setItem(idx, 1, position)
            self.setItem(idx, 2, planned_position)
            self.setItem(idx, 3, amount)
