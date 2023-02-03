from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QButtonGroup,
    QHBoxLayout,
    QSizePolicy,
)
import qtawesome as qta  # type: ignore

from ftt.handlers.portfolio_versions_list_handler import PortfolioVersionsListHandler
from ftt.handlers.portfolios_list_handler import PortfoliosListHandler
from ftt.storage import schemas
from ftt.ui.navigation.views.new_portfolio_dialog import NewPortfolioDialog
from ftt.ui.state import get_state


class NavigationButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlat(True)
        self.setStyleSheet(
            """
            QPushButton, QPushButton:hover {
                height: 20px;
                text-align: left;
                padding: 5px;
            }
            """
        )
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))


class NavigationTilesBuilder:
    @classmethod
    def arrow_tile(cls, *args, **kwargs):
        button = NavigationButton(*args, **kwargs)
        button.setMaximumWidth(30)
        button.setIcon(qta.icon("fa5s.angle-right"))
        return button

    @classmethod
    def build_portfolio_tile(
        cls, portfolio: schemas.Portfolio, parent: QWidget
    ) -> NavigationButton:
        button = NavigationButton(portfolio.name, parent)
        button.setCheckable(True)
        button.setObjectName(portfolio.name)
        button.setProperty("id", portfolio.id)
        button.setProperty("type", "portfolio")
        return button

    @classmethod
    def build_version_tile(
        cls, version: schemas.PortfolioVersion, parent: QWidget
    ) -> NavigationButton:
        button = NavigationButton(version.optimization_strategy_name, parent)
        button.setCheckable(True)
        button.setObjectName(version.optimization_strategy_name)
        button.setProperty("id", version.id)
        button.setProperty("type", "portfolio_version")
        button.setStyleSheet(
            """
            QPushButton {
                text-align: left;
                padding: 4px 4px 4px 20px;
            }
            """
        )
        return button


class PortfolioNavigationTree(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout(self)
        self._button_group = QButtonGroup()
        self._button_group.setExclusive(True)
        self._button_group.idClicked.connect(self._on_button_clicked)
        self._state = get_state()

    def create_ui(self, parent):
        portfolios_result = PortfoliosListHandler().handle()

        if portfolios_result.is_err():
            print(portfolios_result.unwrap_err())
            return

        for portfolio in portfolios_result.unwrap():
            splitbutton = QWidget()
            splitbutton.setLayout(QHBoxLayout())
            splitbutton.layout().setContentsMargins(0, 0, 0, 0)
            splitbutton.layout().setAlignment(Qt.AlignLeft)
            splitbutton.layout().setSpacing(0)

            arrow_button = NavigationTilesBuilder.arrow_tile(self)
            splitbutton.layout().addWidget(arrow_button)

            button = NavigationTilesBuilder.build_portfolio_tile(portfolio, self)
            self._button_group.addButton(button)
            splitbutton.layout().addWidget(button)

            self._layout.addWidget(splitbutton)

            versions_result = PortfolioVersionsListHandler().handle(
                portfolio=schemas.Portfolio(id=portfolio.id)
            )

            if versions_result.is_err():
                print(versions_result.unwrap_err())
                return

            for version in versions_result.unwrap():
                button = NavigationTilesBuilder.build_version_tile(version, self)
                self._button_group.addButton(button)
                self._layout.addWidget(button)

        parent.layout().addWidget(self)

    def _on_button_clicked(self, button_id):
        buttons = self._button_group.buttons()
        for button in buttons:
            if self._button_group.button(button_id) != button:
                button.setChecked(False)

        clicked_button = self._button_group.button(button_id)
        if clicked_button.property("type") == "portfolio":
            self._state.display_portfolio(clicked_button.property("id"))
        elif clicked_button.property("type") == "portfolio_version":
            # self._state.select_portfolio_version(clicked_button.property("id"))
            pass
        else:
            print("Unknown button type")


class NavigationView(QWidget):
    def __init__(self):
        super().__init__()

        self._portfolios_state_group = None
        self._buttons_group = None
        self._layout = None
        self._portfolios_group = None
        self._state = get_state()
        self.create_ui()

    def create_ui(self):
        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)

        label = QLabel("My portfolios")
        label.setMaximumHeight(40)
        label.setMinimumHeight(20)
        self._layout.addWidget(label, 0, alignment=Qt.AlignTop)

        # self.portfoliosListToNavigation()
        PortfolioNavigationTree().create_ui(self)
        # self._state.signals.selectedPortfolioChanged.connect(
        #     self.portfoliosListToNavigation
        # )

        self._layout.addStretch()

        new_portfolio_button = QPushButton("New Portfolio")
        new_portfolio_button.clicked.connect(
            lambda _: self._state.display_new_portfolio_dialog()
        )
        self._layout.addWidget(new_portfolio_button, 0, alignment=Qt.AlignTop)

        dialog = NewPortfolioDialog()
        self._state.signals.newPortfolioDialogDisplayed.connect(lambda: dialog.exec())

    def portfolios_list_to_navigation(self, *_):
        for button in self._portfolios_state_group.buttons():
            self._portfolios_state_group.removeButton(button)

        for button in self._buttons_group.children():
            if type(button) == QPushButton:
                self._buttons_group.layout().removeWidget(button)
                button.setParent(None)
                del button

        result = PortfoliosListHandler().handle()
        if result.is_ok():
            for portfolio in result.unwrap():
                button = QPushButton(portfolio.name)
                button.clicked.connect(
                    lambda *args, o=portfolio.id: self._state.display_portfolio(o)
                )
                self._portfolios_state_group.addButton(button)
                self._buttons_group.layout().addWidget(button)
        else:
            pass
