from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from ftt.ui.central_frame.views import CentralFrameView
from ftt.ui.navigation.models import NavigationModel
from ftt.ui.navigation.views import NavigationView


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(1200, 800))

        self.frame = QWidget(self)
        self.setCentralWidget(self.frame)

        self.setWindowTitle("Financial Trading Tools")
        self.layout = QHBoxLayout(self.frame)

        self.navigation = NavigationView(parent=self.frame, model=NavigationModel())
        self.central_space = CentralFrameView(parent=self.frame, model=None)

        self.layout.addWidget(self.navigation)
        self.layout.addWidget(self.central_space)
