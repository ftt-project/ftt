from PySide6.QtCore import Slot, Signal, Qt
from PySide6.QtGui import QPainter, QBrush, QColor, QPalette
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QLabel, QToolBar, \
    QButtonGroup, QPushButton, QHBoxLayout, QStyle, QGraphicsOpacityEffect, QProgressDialog

from ftt.ui.backtesting.models import BacktestingModel
from ftt.ui.backtesting.views import BacktestingView


class PortfolioVersionsTable(QWidget):
    portfolioVersionSelected = Signal(int)
    portfolioVersionsBacktestRequest = Signal(list)

    BUTTONS = {
        0: "New Version",
        1: "Backtest",
        2: "Remove"
    }

    def __init__(self):
        super().__init__()

        self._versions = []

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._createTable()
        self._createButtonControlls()

    def _createTable(self):
        self._table = QTableWidget()
        self._table.setMaximumHeight(300)

        self._table.setColumnCount(9)
        self._table.setHorizontalHeaderLabels([
            "Optimization Strategy", "Active",
            "Value", "Period Start", "Period End",
            "Interval", "Expected Annual Return", "Annual Volatility",
            "Sharpe Ratio"
        ])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.verticalHeader().setVisible(False)

        self._table.cellClicked.connect(self.onCellClicked)

        self._layout.addWidget(QLabel("<h4>Portfolio Versions</h4>"), 0, alignment=Qt.AlignTop)
        self._layout.addWidget(self._table)

    def _createButtonControlls(self):
        self._buttons_layout = QHBoxLayout()
        self._controls = QButtonGroup()
        self._controls.setExclusive(False)
        for key, value in self.BUTTONS.items():
            button = QPushButton(value)
            button.setEnabled(False)
            self._controls.addButton(button, key)
            self._buttons_layout.addWidget(button)

        self._controls.idClicked.connect(self.onButtonClicked)

        self._layout.addLayout(self._buttons_layout)

    @Slot(int)
    def onButtonClicked(self, button_id):
        match button_id:
            case 0:
                self.onBacktestClicked()
            case 1:
                self.onRemoveClicked()

    def onBacktestClicked(self):
        self.portfolioVersionsBacktestRequest.emit(self._currentTableSelection())
        pass

    def onRemoveClicked(self):
        print("Remove clicked not implemented")
        pass

    @Slot()
    def updateVersionsRows(self, versions):
        self._versions = versions
        self._table.clearContents()
        self._table.setRowCount(len(versions))
        for idx, item in enumerate(versions):
            optimization_strategy_name = QTableWidgetItem(item.optimization_strategy_name)
            active = QTableWidgetItem("Yes" if item.active else "No")
            version = QTableWidgetItem(f"{item.version}")
            period_start = QTableWidgetItem(f"{item.period_start}")
            period_end = QTableWidgetItem(f"{item.period_end}")
            interval = QTableWidgetItem(f"{item.interval}")
            expected_annual_return = QTableWidgetItem('{0:.4g}'.format(item.expected_annual_return or 0))
            annual_volatility = QTableWidgetItem('{0:.4g}'.format(item.annual_volatility or 0))
            sharpe_ratio = QTableWidgetItem("{0:.4g}".format(item.sharpe_ratio or 0))

            self._table.setItem(idx, 0, optimization_strategy_name)
            self._table.setItem(idx, 1, active)
            self._table.setItem(idx, 2, version)
            self._table.setItem(idx, 3, period_start)
            self._table.setItem(idx, 4, period_end)
            self._table.setItem(idx, 5, interval)
            self._table.setItem(idx, 6, expected_annual_return)
            self._table.setItem(idx, 7, annual_volatility)
            self._table.setItem(idx, 8, sharpe_ratio)

    @Slot()
    def onCellClicked(self, row, _):
        selected = self._currentTableSelection()
        print(f"Selected: {selected}")
        if len(selected) == 0:
            [button.setEnabled(False) for button in self._controls.buttons()]
            self.portfolioVersionSelected.emit(-1)
        elif len(selected) == 1:
            [button.setEnabled(True) for button in self._controls.buttons()]
            self.portfolioVersionSelected.emit(selected[0])
        else:
            [button.setEnabled(True) for button in self._controls.buttons()]
            self.portfolioVersionSelected.emit(-1)
            print("Multiple rows selection is not supported yet")

        # self.portfolioVersionSelected.emit([self._versions[idx].id for idx in rows])

    def _currentTableSelection(self):
        """
        Returns a list of portfolio version ids currently selected in table
        """
        return list({self._versions[idx.row()].id for idx in self._table.selectedIndexes()})


class PortfolioVersionWeightsTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self._weights = []
        self.setMinimumHeight(300)
        self.setMaximumHeight(500)

        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Security", "Position", "Planned Position", "Amount"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.verticalHeader().setVisible(False)

    @Slot()
    def updateWeights(self, weights):
        self._weights = weights
        self.clearContents()
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


class CentralPortfolioView(QWidget):
    portfolioVersionsListChanged = Signal()
    weightsListChanged = Signal()

    def __init__(self, model):
        super().__init__()

        self._portfolio = None
        self._weights_table = None
        self._versions_table = None
        self._current_portfolio_version_weights = None
        self._portfolio_versions = None
        self._model = model

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)

        self.createTopBar()
        self.createVersionsTable()
        self.createWeightsTable()

    def createTopBar(self):
        self._top_bar = QHBoxLayout()
        self._top_bar_header = QLabel("")
        self._top_bar.addWidget(self._top_bar_header)

        self._top_controls_layout = QHBoxLayout()
        self._top_controls = QButtonGroup()
        self._top_controls.setExclusive(False)
        self._top_controls_layout.setAlignment(Qt.AlignRight)

        sync_button = QPushButton("Synchronize with broker")
        sync_button.setEnabled(True)
        sync_button.clicked.connect(self.onSyncClicked)
        self._top_controls.addButton(sync_button, 0)
        self._top_controls_layout.addWidget(sync_button)

        sync_button_help = QPushButton()
        sync_button_help.setIcon(sync_button_help.style().standardIcon(QStyle.SP_MessageBoxInformation))
        self._top_controls.addButton(sync_button_help, 1)
        self._top_controls_layout.addWidget(sync_button_help)

        self._top_bar.addLayout(self._top_controls_layout)
        self._layout.addLayout(self._top_bar)

    def createVersionsTable(self):
        self._versions_table = PortfolioVersionsTable()
        self._layout.addWidget(self._versions_table, 0, alignment=Qt.AlignTop)
        self.portfolioVersionsListChanged.connect(
            lambda: self._versions_table.updateVersionsRows(self._portfolio_versions)
        )

        self._versions_table.portfolioVersionSelected.connect(self.onPortfolioVersionSelected)
        self._versions_table.portfolioVersionsBacktestRequest.connect(self.onPortfolioVersionsBacktestRequest)
        
    def createWeightsTable(self):
        self._layout.addWidget(QLabel("<h4>Weights</h4>"), 0, alignment=Qt.AlignTop)
        self._weights_table = PortfolioVersionWeightsTable()
        self._layout.addWidget(self._weights_table, 0, alignment=Qt.AlignTop)
        self.weightsListChanged.connect(
            lambda: self._weights_table.updateWeights(self._current_portfolio_version_weights)
        )
        self.portfolioVersionsListChanged.connect(
            lambda: self._weights_table.updateWeights([])
        )

    @Slot()
    def onSyncClicked(self):
        progress = QProgressDialog("Synchronizing with broker system...", "Abort", 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        
    @Slot(int)
    def onPortfolioChanged(self, portfolio_id):
        print(f"Portfolio changed: {portfolio_id}")
        self._portfolio = self._model.getPortfolio(portfolio_id)
        self._portfolio_versions = self._model.getPortfolioVersions(portfolio_id)
        self._top_bar_header.setText(f"<h3>{self._portfolio.name}</h3>")
        self.portfolioVersionsListChanged.emit()

    @Slot(int)
    def onPortfolioVersionSelected(self, portfolio_version_id):
        print(f"Portfolio version selected: {portfolio_version_id}")
        if portfolio_version_id == -1:
            self._current_portfolio_version_weights = []
        else:
            self._current_portfolio_version_weights = self._model.getPortfolioVersionWeights(portfolio_version_id)
        self.weightsListChanged.emit()

    @Slot(list)
    def onPortfolioVersionsBacktestRequest(self, portfolio_version_ids):
        model = BacktestingModel(portfolio_version_ids=portfolio_version_ids)
        self.backtesting_view = BacktestingView(model)
        self.backtesting_view.show()