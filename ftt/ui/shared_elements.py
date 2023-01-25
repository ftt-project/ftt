from datetime import datetime

from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QFrame,
    QVBoxLayout,
    QLineEdit,
    QDateEdit,
    QComboBox,
)


class H1QLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("font-size: 20px; font-weight: bold;")


class H2QLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("font-size: 16px;")


class H1QSeparator(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameStyle(QFrame.HLine | QFrame.NoFrame)
        self.setFixedHeight(30)


_mapper = {
    "h1": (H1QLabel, H1QSeparator),
    "h2": (H2QLabel, H1QSeparator),
}


class StyledLabelComponent(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

    def setText(self, text):
        self.findChild(QLabel).setText(text)


class LabelBuilder:
    @classmethod
    def h1_build(cls, text: str, parent: QWidget = None) -> QWidget:
        return cls.build("h1", text, parent)

    @classmethod
    def h2_build(cls, text: str, parent: QWidget = None) -> QWidget:
        return cls.build("h2", text, parent)

    @classmethod
    def build(cls, size: str, text: str, parent: QWidget = None) -> QWidget:
        label_class, separator_class = _mapper[size]
        wrapper = StyledLabelComponent(parent)
        wrapper.layout().addWidget(label_class(text))
        wrapper.layout().addWidget(separator_class())

        return wrapper


class EditElementInterface:
    def valid(self) -> bool:
        return True


class NoFrameLineEdit(QLineEdit, EditElementInterface):
    inputChanged = Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setFrame(False)

        self.setObjectName(kwargs.get("object_name", ""))
        self.setPlaceholderText(kwargs.get("placeholder", ""))
        self.setValidator(kwargs.get("validator", None))
        self.setText(kwargs.get("initial_value", None))

        self.textChanged.connect(self.inputChanged)

    def valid(self) -> bool:
        return self.hasAcceptableInput()


class NoFrameDateEdit(QDateEdit, EditElementInterface):
    inputChanged = Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setFrame(False)

        initial_value = kwargs.get("initial_value", None)
        if isinstance(initial_value, QDate):
            self.setDate(initial_value)
        elif isinstance(initial_value, datetime):
            d = QDate()
            d.setDate(initial_value.year, initial_value.month, initial_value.day)
            self.setDate(d)

        self.setObjectName(kwargs.get("object_name", ""))
        self.setDisplayFormat("yyyy-MM-dd")
        self.setCalendarPopup(True)
        self.setMaximumDate(kwargs.get("max_date", QDate(9999, 12, 31)))
        self.setMinimumDate(kwargs.get("min_date", QDate(1900, 1, 1)))

        self.dateChanged.connect(self.inputChanged)

    def valid(self) -> bool:
        return self.hasAcceptableInput()


class ComboBoxEdit(QComboBox, EditElementInterface):
    inputChanged = Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setFrame(False)

        self.setObjectName(kwargs.get("object_name", ""))
        self.addItems(kwargs.get("items", []))

        self.currentTextChanged.connect(self.inputChanged)
        self.setCurrentText(kwargs.get("initial_value", None))
