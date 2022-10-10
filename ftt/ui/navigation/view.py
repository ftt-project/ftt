from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QButtonGroup
from result import Ok, Err

from ftt.handlers.portfolios_list_handler import PortfoliosListHandler
from ftt.ui.navigation.models import NavigationModel
from ftt.ui.navigation.views.new_portfolio_dialog import NewPortfolioDialog


class NavigationSignals(QObject):
    portfolioRequested = Signal(int)


class NavigationView(QWidget):
    def __init__(self):
        super().__init__()

        self._portfolios_state_group = None
        self._buttons_group = None
        self._layout = None
        self._portfolios_group = None
        self._model = NavigationModel()
        self.signals = NavigationSignals()
        self.createUI()

    def createUI(self):
        self.setMaximumWidth(300)

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)

        label = QLabel("Portfolios")
        label.setMaximumHeight(40)
        label.setMinimumHeight(20)
        self._layout.addWidget(label, 0, alignment=Qt.AlignTop)

        self._portfolios_state_group = QButtonGroup()
        self._portfolios_state_group.setExclusive(True)

        self._buttons_group = QWidget()
        self._buttons_group.setLayout(QVBoxLayout())
        self._layout.addWidget(self._buttons_group)

        self.portfoliosListToNavigation()

        self._layout.addStretch()

        new_portfolio_button = QPushButton("New Portfolio")
        new_portfolio_button.clicked.connect(self.onNewPortfolioClicked)
        self._layout.addWidget(new_portfolio_button, 0, alignment=Qt.AlignTop)

    def portfoliosListToNavigation(self, *_):
        for button in self._portfolios_state_group.buttons():
            self._portfolios_state_group.removeButton(button)

        for button in self._buttons_group.children():
            if type(button) == QPushButton:
                self._buttons_group.layout().removeWidget(button)

        result = PortfoliosListHandler().handle()
        match result:
            case Ok(portfolios):
                for portfolio in portfolios:
                    button = QPushButton(portfolio.name)
                    button.clicked.connect(
                        lambda *args, o=portfolio.id: self.displayPortfolioById(o)
                    )
                    self._portfolios_state_group.addButton(button)
                    self._buttons_group.layout().addWidget(button)
            case Err():
                pass

    def displayPortfolioById(self, portfolio_id):
        self._model.currentPortfolioId = portfolio_id
        self.signals.portfolioRequested.emit(portfolio_id)

    def onNewPortfolioClicked(self):
        dialog = NewPortfolioDialog()
        dialog.signals.newPortfolioCreated.connect(self.portfoliosListToNavigation)
        dialog.signals.newPortfolioCreated.connect(self.signals.portfolioRequested)
        dialog.exec()
