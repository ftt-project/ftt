from PySide6.QtCore import Slot
from PySide6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem

from ftt.ui.portfolio.models import get_model
from ftt.ui.portfolio.signals import PortfolioSignals


class PortfolioVersionWeightsTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.signals = PortfolioSignals()
        self._model = get_model()

        self.createUI()

        self.signals.portfolioVersionSelected.connect(self.onPortfolioVersionSelected)

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

    @Slot(int)
    def onPortfolioVersionSelected(
        self, portfolio_version_id
    ):  # noqa: F811  # type: ignore
        print(f"Portfolio version selected: {portfolio_version_id}")
        if portfolio_version_id is None:
            self.updateWeights()
        return

    @Slot(list)
    def onPortfolioVersionSelected(self, portfolio_version_ids):  # noqa: F811
        print(f"Portfolio version selected: {portfolio_version_ids}")
        self._model.currentPortfolioVersionId = portfolio_version_ids
        self.updateWeights()

    def updateWeights(self):
        self.clearContents()
        if (
            self._model.currentPortfolioVersionId is None
            or self._model.currentPortfolioVersionId == -1
        ):
            return
        weights = self._model.getPortfolioVersionWeights()
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
