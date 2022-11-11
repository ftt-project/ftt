from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QButtonGroup
from result import Ok, Err

from ftt.handlers.portfolios_list_handler import PortfoliosListHandler
from ftt.ui.navigation.views.new_portfolio_dialog import NewPortfolioDialog
from ftt.ui.state import get_state


class NavigationView(QWidget):
    def __init__(self):
        super().__init__()

        self._portfolios_state_group = None
        self._buttons_group = None
        self._layout = None
        self._portfolios_group = None
        self._state = get_state()
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
        self._state.signals.selectedPortfolioChanged.connect(
            self.portfoliosListToNavigation
        )

        self._layout.addStretch()

        new_portfolio_button = QPushButton("New Portfolio")
        new_portfolio_button.clicked.connect(
            lambda _: self._state.display_new_portfolio_dialog()
        )
        self._layout.addWidget(new_portfolio_button, 0, alignment=Qt.AlignTop)

        dialog = NewPortfolioDialog()
        self._state.signals.newPortfolioDialogDisplayed.connect(lambda: dialog.exec())

    def portfoliosListToNavigation(self, *_):
        for button in self._portfolios_state_group.buttons():
            self._portfolios_state_group.removeButton(button)

        for button in self._buttons_group.children():
            if type(button) == QPushButton:
                self._buttons_group.layout().removeWidget(button)
                button.setParent(None)
                del button

        result = PortfoliosListHandler().handle()
        match result:
            case Ok(portfolios):
                for portfolio in portfolios:
                    button = QPushButton(portfolio.name)
                    button.clicked.connect(
                        lambda *args, o=portfolio.id: self._state.display_portfolio(o)
                    )
                    self._portfolios_state_group.addButton(button)
                    self._buttons_group.layout().addWidget(button)
            case Err():
                pass
