from PySide6.QtCore import Slot, Signal, QObject
from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout

from ftt.ui.navigation.view import NavigationView
from ftt.ui.portfolio.view import CentralPortfolioView


class MainWindowSignals(QObject):
    """
    Defines the signals available for a main window.

    Supported signals are:

    portfolioChanged
        int portfolio id
    """

    portfolioChanged = Signal(int)


class MainWidget(QWidget):
    currentPortfolioChanged = Signal(int)

    def __init__(self):
        super().__init__()

        self.signals = MainWindowSignals()

        self._navigation = None
        self._layout = None
        self._center = None

        self.createUI()

    def createUI(self):
        self._layout = QHBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)

        self._navigation = NavigationView()
        self._layout.addWidget(self._navigation)

        self._center = CentralPortfolioView()
        self._layout.addWidget(self._center)

        self._navigation.signals.portfolioRequested.connect(
            self._center.signals.portfolioChanged
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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
