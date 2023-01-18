from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel, QFrame

from ftt.handlers.portfolio_handlers import PortfolioLoadHandler
from ftt.storage import schemas
from ftt.ui.model import get_model
from ftt.ui.portfolio.views.portfolio_details_widget import PortfolioDetailsWidget
from ftt.ui.portfolio.views.portfolio_versions_widget import PortfolioVersionsWidget
from ftt.ui.state import get_state


class CentralPortfolioView(QWidget):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget(self)
        self.layout = QVBoxLayout(self)
        self.portfolio_name_label = QLabel()
        self._model = get_model()
        self._state = get_state()
        self.create_ui()

    def create_ui(self):
        self.portfolio_name_label.setStyleSheet("font-size: 20px")

        self._state.signals.selectedPortfolioChanged.connect(
            self.update_portfolio_name_label
        )

        self.layout.addWidget(self.portfolio_name_label)

        separator = QFrame()
        separator.setFixedHeight(30)
        separator.setFrameStyle(QFrame.HLine | QFrame.NoFrame)
        self.layout.addWidget(separator)

        self.layout.addWidget(self.tabs)

        self.tabs.addTab(
            PortfolioVersionsWidget(),
            "Versions"
        )

        self.tabs.addTab(
            PortfolioDetailsWidget(),
            "Portfolio Details"
        )

    def update_portfolio_name_label(self):
        result = PortfolioLoadHandler().handle(
            portfolio=schemas.Portfolio(id=self._model.portfolio_id)
        )
        if result.is_err():
            print(result.err())
            return

        self.portfolio_name_label.setText(result.unwrap().name)


