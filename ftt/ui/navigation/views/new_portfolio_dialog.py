from PySide6.QtCore import Signal
from PySide6.QtGui import QValidator, Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QDialogButtonBox,
    QVBoxLayout,
    QWidget,
)
from result import Ok, Err

from ftt.handlers.portfolio_creation_handler import PortfolioCreationHandler


class PortfolioNameValidator(QValidator):
    def validate(self, text, pos):
        if len(text) < 2:
            return QValidator.Intermediate
        elif len(text) >= 30:
            return QValidator.Invalid
        else:
            return QValidator.Acceptable


class NewPortfolioDialog(QDialog):
    newPortfolioCreated = Signal()

    def __init__(self):
        super().__init__()

        self._hint_message = None
        self._buttons = None
        self._name_field = None
        self._label = None
        self._layout = None
        self.createUI()

    def createUI(self):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        widget = QWidget()
        self._layout.addWidget(widget)
        form_layout = QHBoxLayout(widget)

        self._label = QLabel("Portfolio Name")
        self._name_field = QLineEdit()
        self._name_field.setMinimumWidth(250)
        self._name_field.setValidator(PortfolioNameValidator())

        form_layout.addWidget(self._label)
        form_layout.addWidget(self._name_field)

        self._hint_message = QLabel("")
        self._layout.addWidget(self._hint_message)
        self._hint_message.setAlignment(Qt.AlignRight)
        self._hint_message.hide()

        self._buttons = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.Cancel)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def accept(self) -> None:
        if self._name_field.hasAcceptableInput():
            name = self._name_field.text()
            result = PortfolioCreationHandler().handle(name=name)
            match result:
                case Ok(portfolio):
                    self.newPortfolioCreated.emit()
                    super().accept()
                case Err():
                    self._hint_message.setText(result.unwrap_err())
                    self._hint_message.show()
        else:
            self._hint_message.setText("Name portfolio 2 - 50 symbols length")
            self._hint_message.show()

    def reject(self) -> None:
        super().reject()
