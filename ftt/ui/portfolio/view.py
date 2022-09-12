from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from ftt.ui.portfolio.signals import PortfolioSignals
from ftt.ui.portfolio.views.portfolio_version_details_views import PortfolioVersionDetailsView
from ftt.ui.portfolio.views.portfolio_version_weights_table import PortfolioVersionWeightsTable
from ftt.ui.portfolio.views.portfolio_versions_table import PortfolioVersionsTable


class CentralPortfolioView(QWidget):
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
        self.signals.portfolioChanged.connect(self._portfolioVersionDetails.signals.portfolioChanged)
        self._portfolioVersionsTable.signals.portfolioVersionSelected.connect(
            self._portfolioVersionDetails.signals.portfolioVersionSelected
        )

        layout.addWidget(left_column)
        layout.addWidget(right_column)

