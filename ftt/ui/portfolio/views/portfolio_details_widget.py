from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class PortfolioDetailsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout(self)
        self._label = None

        self.create_ui()

    def create_ui(self):
        self._label = QLabel("Portfolio Details")
        self._layout.addWidget(self._label, 0, alignment=Qt.AlignTop)