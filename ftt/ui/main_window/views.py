from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QApplication,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QStyleFactory,
)

from ftt.ui.navigation.view import NavigationView
from ftt.ui.portfolio.view import CentralPortfolioView
from ftt.ui.state import get_state


class WelcomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._label = None
        self._layout = None

        self.createUI()

    def createUI(self):
        self._layout = QHBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)

        self._label = QLabel("Welcome to FTT")

        self._layout.addWidget(self._label)


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._navigation = None
        self._layout = None
        self._center = None
        self._state = get_state()

        self.create_ui()

    def create_ui(self):
        self._layout = QHBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)

        self._navigation = NavigationView()
        self._layout.addWidget(self._navigation)

        self._center = QStackedWidget()
        self._center.addWidget(WelcomeWidget())
        self._center.addWidget(CentralPortfolioView())
        self._center.setCurrentIndex(0)

        self._layout.addWidget(self._center)

        self._state.signals.selectedPortfolioChanged.connect(
            lambda: self._center.setCurrentIndex(1)
        )
        self._state.signals.welcomeScreenDisplayed.connect(
            lambda: self._center.setCurrentIndex(0)
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QApplication.setStyle(QStyleFactory.create("Fusion"))

        self.setWindowTitle("Financial Trading Tool")
        self.resize(1400, 800)

        widget = MainWidget()

        button_action = QAction("&Create new", self)
        about_action = QAction("&Program", self)

        menu = self.menuBar()

        file_menu = menu.addMenu("&Portfolio")
        file_menu.addAction(button_action)

        about_menu = menu.addMenu("&Help")
        about_menu.addAction(about_action)

        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()
