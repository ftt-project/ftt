from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget, QVBoxLayout


class PortfolioView(QWidget):
    def __init__(self):
        super().__init__()
        self.label1 = QLabel("Portfolio")
        self.label2 = QLabel("The best of course")

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)

        self.setLayout(layout)
