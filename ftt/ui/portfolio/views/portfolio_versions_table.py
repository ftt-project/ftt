from collections import namedtuple

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import (
    QTableWidgetItem,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QPushButton,
    QHeaderView,
    QVBoxLayout,
    QWidget
)

from ftt.ui.portfolio.models import get_model
from ftt.ui.portfolio.signals import PortfolioSignals
from ftt.ui.portfolio.views.new_portfolio_version_dialog import NewPortfolioVersionDialog


class PortfolioVersionsTable(QWidget):
    def __init__(self):
        super().__init__()

        self.signals = PortfolioSignals()
        self._model = get_model()

        self._buttons = None
        self._layout = None
        self._table = None

        self.createUI()

        self.signals.portfolioChanged.connect(self.onPortfolioChanged)

    def createUI(self):
        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._table = QTableWidget()
        self._table.setMaximumHeight(300)
        self._table.setMinimumWidth(1000)

        self._table.setColumnCount(9)
        self._table.setHorizontalHeaderLabels(
            [
                "Optimization Strategy",
                "Active",
                "Value",
                "Period Start",
                "Period End",
                "Interval",
                "Expected Annual Return",
                "Annual Volatility",
                "Sharpe Ratio",
            ]
        )
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.verticalHeader().setVisible(False)

        self._table.cellClicked.connect(self.onCellFocusChange)

        self._layout.addWidget(
            QLabel("<h4>Portfolio Versions</h4>"), 0, alignment=Qt.AlignTop
        )
        self._layout.addWidget(self._table)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)

        self._buttons = namedtuple("Buttons", "new_version, remove_version")  # Ugly, really using comma?

        self._buttons.new_version = QPushButton("New Version")
        self._buttons.new_version.clicked.connect(self.onNewVersionClicked)
        buttons_layout.addWidget(self._buttons.new_version, 0)

        self._buttons.remove_version = QPushButton("Remove selected")
        self._buttons.remove_version.setEnabled(False)
        self._buttons.remove_version.clicked.connect(self.onRemoveClicked)
        buttons_layout.addWidget(self._buttons.remove_version, 0)

        self._layout.addLayout(buttons_layout)

    def onNewVersionClicked(self):
        dialog = NewPortfolioVersionDialog()
        dialog.signals.newPortfolioVersionCreated.connect(self.onPortfolioListChanged)
        dialog.exec()

    def onRemoveClicked(self):
        print("Remove clicked not implemented")
        pass

    def _currentTableSelection(self):
        """
        Returns a list of portfolio version ids currently selected in table
        """
        versions = self._model.getPortfolioVersions()
        return list({versions[idx.row()].id for idx in self._table.selectedIndexes()})

    @Slot(int)
    def onPortfolioChanged(self, portfolio_id):
        self._model.currentPortfolioId = portfolio_id
        self.updateVersionsRows()

    def onPortfolioListChanged(self, portfolio_version_id):
        self._model.currentPortfolioVersionId = portfolio_version_id
        self.updateVersionsRows()

    @Slot()
    def updateVersionsRows(self):
        versions = self._model.getPortfolioVersions()
        self._table.clearContents()
        self._table.setRowCount(len(versions))
        row_to_focus = None
        item_scroll_to = None
        for idx, item in enumerate(versions):
            optimization_strategy_name = QTableWidgetItem(
                item.optimization_strategy_name
            )
            active = QTableWidgetItem("Yes" if item.active else "No")
            value = QTableWidgetItem(f"{item.value}")
            period_start = QTableWidgetItem(f"{item.period_start}")
            period_end = QTableWidgetItem(f"{item.period_end}")
            interval = QTableWidgetItem(f"{item.interval}")
            expected_annual_return = QTableWidgetItem(
                "{0:.4g}".format(item.expected_annual_return or 0)
            )
            annual_volatility = QTableWidgetItem(
                "{0:.4g}".format(item.annual_volatility or 0)
            )
            sharpe_ratio = QTableWidgetItem("{0:.4g}".format(item.sharpe_ratio or 0))

            self._table.setItem(idx, 0, optimization_strategy_name)
            self._table.setItem(idx, 1, active)
            self._table.setItem(idx, 2, value)
            self._table.setItem(idx, 3, period_start)
            self._table.setItem(idx, 4, period_end)
            self._table.setItem(idx, 5, interval)
            self._table.setItem(idx, 6, expected_annual_return)
            self._table.setItem(idx, 7, annual_volatility)
            self._table.setItem(idx, 8, sharpe_ratio)

            # identify already selected row. Focus on newly created version
            if item.id == self._model.currentPortfolioVersionId:
                row_to_focus = idx
                item_scroll_to = optimization_strategy_name

        if row_to_focus is not None:
            self._table.selectRow(row_to_focus)
            self._table.scrollToItem(item_scroll_to)
            self.onCellFocusChange()

    @Slot()
    def onCellFocusChange(self, *_):
        # TODO on portfolio change "remove selected" is not disabled
        selected = self._currentTableSelection()
        print(f"Selected: {selected}")
        if len(selected) == 0:
            self._buttons.remove_version.setEnabled(False)
            self.signals.portfolioVersionSelected.emit(-1)
        elif len(selected) == 1:
            self._buttons.remove_version.setEnabled(True)
            self.signals.portfolioVersionSelected.emit(selected[0])
        else:
            self._buttons.remove_version.setEnabled(True)
            self.signals.portfolioVersionSelected.emit(-1)
            print("Multiple rows selection is not supported yet")
