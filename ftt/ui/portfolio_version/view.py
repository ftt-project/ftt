from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStyle, QHBoxLayout


class PortfolioVersionDetailsView(QWidget):
    def __init__(self, model):
        super().__init__()
        self._model = model

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.setAlignment(Qt.AlignTop)

        self.setMaximumWidth(400)

        self._createConrols()

    def _createConrols(self):
        self._edit_button = QPushButton("Edit")
        self._rebalance_button = QPushButton("Rebalance")
        self._backtesting_button = QPushButton("Run Backtesting")

        self._active_button = QPushButton("Active")
        self._synch_button = QPushButton("Synchronize with broker")
        self._sync_button_help = QPushButton()
        self._sync_button_help.setIcon(self._sync_button_help.style().standardIcon(QStyle.SP_MessageBoxInformation))

        first_row_layout = QHBoxLayout()
        first_row_layout.addWidget(self._rebalance_button)
        first_row_layout.addWidget(self._edit_button)
        first_row_layout.addWidget(self._backtesting_button)
        self._layout.addLayout(first_row_layout)

        second_row_layout = QHBoxLayout()
        second_row_layout.addWidget(self._active_button)
        second_row_layout.addWidget(self._synch_button)
        second_row_layout.addWidget(self._sync_button_help)
        self._layout.addLayout(second_row_layout)