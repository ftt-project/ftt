from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from result import Ok

from ftt.handlers.portfolios_list_handler import PortfoliosListHandler
from ftt.ui.navigation.models import NavigationModel


class NavigationSignals(QObject):
    portfolioRequested = Signal(int)


class NavigationView(QWidget):
    def __init__(self):
        super().__init__()

        self._model = NavigationModel()
        self.signals = NavigationSignals()
        self.createUI()

    def createUI(self):
        self.setMaximumWidth(300)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        label = QLabel("Portfolios")
        label.setMaximumHeight(40)
        label.setMinimumHeight(20)
        layout.addWidget(label, 0, alignment=Qt.AlignTop)
        result = PortfoliosListHandler().handle()
        match result:
            case Ok(portfolios):
                for portfolio in portfolios:
                    button = QPushButton(portfolio.name)
                    button.clicked.connect(
                        lambda *args, o=portfolio.id: self.onPortfolioClicked(o)
                    )
                    layout.addWidget(button, 0, alignment=Qt.AlignTop)
        layout.addStretch()

        layout.addWidget(QPushButton("New Portfolio"), 0, alignment=Qt.AlignTop)

    def onPortfolioClicked(self, portfolio_id):
        self._model.currentPortfolioId = portfolio_id
        self.signals.portfolioRequested.emit(portfolio_id)
