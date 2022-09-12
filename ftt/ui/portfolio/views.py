from PySide6.QtCore import Slot, Signal, Qt, QObject
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QLabel, \
    QButtonGroup, QPushButton, QHBoxLayout

from ftt.ui.backtesting.models import BacktestingModel
from ftt.ui.backtesting.views import BacktestingView
from ftt.ui.portfolio.models import PortfolioModel, get_model
from ftt.ui.portfolio_version.models import PortfolioVersionModel
from ftt.ui.portfolio_version.view import PortfolioVersionDetailsView


class PortfolioSignals(QObject):
    portfolioChanged = Signal(int)
    portfolioVersionSelected = Signal(int)
    # portfolioVersionsBacktestRequest = Signal(list)


class PortfolioVersionsTable(QWidget):
    portfolioVersionSelected = Signal(int)
    portfolioVersionsBacktestRequest = Signal(list)

    BUTTONS = {
        0: "New Version",
        2: "Remove"
    }

    def __init__(self):
        super().__init__()

        self.signals = PortfolioSignals()
        self._model = get_model()

        self._controls = None
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

        buttons_layout = QHBoxLayout()
        self._controls = QButtonGroup()
        self._controls.setExclusive(False)
        for key, value in self.BUTTONS.items():
            button = QPushButton(value)
            button.setEnabled(False)
            self._controls.addButton(button, key)
            buttons_layout.addWidget(button)

        self._controls.idClicked.connect(self.onButtonClicked)

        self._layout.addLayout(buttons_layout)

    def onNewVersionClicked(self):
        print("New version clicked not implemented")
        pass

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

    @Slot(int)
    def onButtonClicked(self, button_id):
        match button_id:
            case 0:
                self.onNewVersionClicked()
            case 1:
                self.onRemoveClicked()

    @Slot()
    def updateVersionsRows(self):
        versions = self._model.getPortfolioVersions()
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
            self.signals.portfolioVersionSelected.emit(-1)
        elif len(selected) == 1:
            [button.setEnabled(True) for button in self._controls.buttons()]
            self.signals.portfolioVersionSelected.emit(selected[0])
        else:
            [button.setEnabled(True) for button in self._controls.buttons()]
            self.signals.portfolioVersionSelected.emit(-1)
            print("Multiple rows selection is not supported yet")

        # self.portfolioVersionSelected.emit([self._versions[idx].id for idx in rows])


class PortfolioVersionWeightsTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.signals = PortfolioSignals()
        self._model = get_model()

        self.createUI()

        self.signals.portfolioChanged.connect(self.onPortfolioChanged)
        self.signals.portfolioVersionSelected.connect(self.onPortfolioVersionSelected)

    def createUI(self):
        self.setMinimumHeight(300)
        self.setMaximumHeight(500)

        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Security", "Position", "Planned Position", "Amount"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.verticalHeader().setVisible(False)

    @Slot(int)
    def onPortfolioChanged(self, portfolio_id):
        self._model.currentPortfolioId = portfolio_id

    @Slot(int)
    def onPortfolioVersionSelected(self, portfolio_version_id):
        print(f"Portfolio version selected: {portfolio_version_id}")
        return

    @Slot(list)
    def onPortfolioVersionSelected(self, portfolio_version_ids):
        print(f"Portfolio version selected: {portfolio_version_ids}")
        self._model.currentPortfolioVersionId = portfolio_version_ids
        self.updateWeights()

    def updateWeights(self):
        weights = self._model.getPortfolioVersionWeights()
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
    currentPortfolioChanged = Signal(int)
    currentPortfolioVersionChanged = Signal(int)

    def __init__(self):
        super().__init__()

        self._portfolioVersionDetails = None
        self._portfolioHeaderLabel = None
        self._portfolioWeightsTable = None
        self._portfolioVersionsTable = None
        self.signals = PortfolioSignals()

        self.createUI()

    def createUI(self):
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        left_column = QWidget()
        left_column_layout = QVBoxLayout(left_column)
        
        right_column = QWidget()
        right_column_layout = QHBoxLayout(right_column)
        
        self._portfolioHeaderLabel = QLabel("")
        left_column_layout.addWidget(self._portfolioHeaderLabel)
        
        self._portfolioVersionsTable = PortfolioVersionsTable()
        left_column_layout.addWidget(self._portfolioVersionsTable, 0, alignment=Qt.AlignTop)
        self.signals.portfolioChanged.connect(self._portfolioVersionsTable.signals.portfolioChanged)

        self._portfolioWeightsTable = PortfolioVersionWeightsTable()
        left_column_layout.addWidget(QLabel("<h4>Weights</h4>"), 0, alignment=Qt.AlignTop)
        left_column_layout.addWidget(self._portfolioWeightsTable, 0, alignment=Qt.AlignTop)
        self.signals.portfolioChanged.connect(self._portfolioWeightsTable.signals.portfolioChanged)
        self._portfolioVersionsTable.signals.portfolioVersionSelected.connect(
            self._portfolioWeightsTable.signals.portfolioVersionSelected
        )

        self._portfolioVersionDetails = PortfolioVersionDetailsView()
        right_column_layout.addWidget(self._portfolioVersionDetails, 0, alignment=Qt.AlignTop)
        # self.signals.portfolioChanged.connect(self._portfolioVersionDetails.signals.portfolioChanged)

        layout.addWidget(left_column)
        layout.addWidget(right_column)

    @Slot(int)
    def onPortfolioChanged(self, portfolio_id):
        self.currentPortfolioChanged.emit(portfolio_id)