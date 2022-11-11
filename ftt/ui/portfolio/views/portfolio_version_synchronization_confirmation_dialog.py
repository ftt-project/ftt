from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QDialogButtonBox,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
)

from ftt.ui.model import get_model


class PortfolioVersionChangesTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self._model = get_model()

        self.createUI()

    def createUI(self):
        self.setMinimumHeight(300)
        self.setMaximumHeight(500)
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)

        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Security", "Delta", "Operation", "Amount"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.verticalHeader().setVisible(False)

    def updateChanges(self):
        changes = self._model.currentPortfolioVersionChanges
        self.clearContents()
        self.setRowCount(len(changes))
        for idx, item in enumerate(changes):
            security = QTableWidgetItem(item["symbol"])
            delta = QTableWidgetItem(f"{item['delta']}")
            operation = QTableWidgetItem(item["operation"])
            amount = QTableWidgetItem(f"{item['amount']}")

            self.setItem(idx, 0, security)
            self.setItem(idx, 1, delta)
            self.setItem(idx, 2, operation)
            self.setItem(idx, 3, amount)


class PortfolioVersionSynchronizationConfirmationDialog(QDialog):
    def __init__(self):
        super().__init__()

        self._table = None
        self._buttons = None
        self._layout = None
        self._model = get_model()

        self.createUI()

    def createUI(self):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._layout.addWidget(
            QLabel(
                "Are you sure you want to synchronize your portfolio with your broker?"
            )
        )

        self._table = PortfolioVersionChangesTable()
        self._table.updateChanges()
        self._layout.addWidget(self._table)

        self._buttons = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.Cancel)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)
