from PySide6.QtCore import Slot, Signal
from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QApplication, QHBoxLayout, QVBoxLayout, QBoxLayout, \
    QPushButton, QTableWidget, QHeaderView
from result import Ok

from ftt.handlers.portfolios_list_handler import PortfoliosListHandler
from ftt.ui.portfolio.models import PortfolioVersionsModel
from ftt.ui.portfolio.views import CentralPortfolioView


class MainWidget(QWidget):
    currentPortfolioChanged = Signal(int)

    def __init__(self, model):
        super().__init__()
        self._model = model

        self.createLayout()
        self.createLeftSide()
        self.createCenterSide()
        self.createRightSide()

    def createLayout(self):
        self._layout = QHBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)
        self.setLayout(self._layout)
        return QHBoxLayout()

    def createLeftSide(self):
        self._left = QWidget()
        self._left.setMaximumWidth(300)
        self._left_layout = QVBoxLayout(self._left)
        self._left_layout.setAlignment(Qt.AlignTop)

        label = QLabel("Portfolios")
        label.setMaximumHeight(40)
        label.setMinimumHeight(20)
        self._left_layout.addWidget(label, 0, alignment=Qt.AlignTop)
        result = PortfoliosListHandler().handle()
        match result:
            case Ok(portfolios):
                for portfolio in portfolios:
                    button = QPushButton(portfolio.name)
                    button.clicked.connect(lambda *args, o=portfolio.id: self.onPortfolioClicked(o))
                    self._left_layout.addWidget(button, 0, alignment=Qt.AlignTop)
        self._left_layout.addStretch()

        self._layout.addWidget(self._left)

    def onPortfolioClicked(self, portfolio_id):
        self._model.onPortfolioClicked(portfolio_id)
        self.currentPortfolioChanged.emit(portfolio_id)

    def createCenterSide(self):
        model = PortfolioVersionsModel()
        self._center = CentralPortfolioView(model)
        self.currentPortfolioChanged.connect(self._center.onPortfolioChanged)

        self._layout.addWidget(self._center)

    def createRightSide(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self.setWindowTitle("FTT")
        self.resize(800, 600)

        widget = MainWidget(model)

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
