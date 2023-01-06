from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from ftt.ui.portfolio.views.portfolio_version_details_views import (
    PortfolioVersionDetailsView,
)
from ftt.ui.portfolio.views.portfolio_version_weights_table import (
    PortfolioVersionWeightsTable,
)
from ftt.ui.portfolio.views.portfolio_versions_table import PortfolioVersionsTable
from ftt.ui.state import get_state


class CentralPortfolioView(QWidget):
    def __init__(self):
        super().__init__()

        self._portfolioVersionDetails = None
        self._portfolioHeaderLabel = None
        self._portfolioWeightsTable = None
        self._portfolioVersionsTable = None
        self._state = get_state()

        self.createUI()

    def createUI(self):
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        left_column = QWidget()
        left_column.setLayout(QVBoxLayout())
        left_column.layout().setAlignment(Qt.AlignTop)
        left_column.layout().setStretch(0, 0)

        right_column = QWidget()
        right_column_layout = QHBoxLayout(right_column)

        self._portfolioHeaderLabel = QLabel("")
        left_column.layout().addWidget(self._portfolioHeaderLabel)

        self._portfolioVersionsTable = PortfolioVersionsTable()
        left_column.layout().addWidget(
            self._portfolioVersionsTable, 0, alignment=Qt.AlignTop
        )

        self._portfolioWeightsTable = PortfolioVersionWeightsTable()
        left_column.layout().addWidget(
            self._portfolioWeightsTable, 0, alignment=Qt.AlignTop
        )

        self._portfolioVersionDetails = PortfolioVersionDetailsView()
        right_column_layout.addWidget(
            self._portfolioVersionDetails, 0, alignment=Qt.AlignTop
        )

        layout.addWidget(left_column)
        layout.addWidget(right_column)
