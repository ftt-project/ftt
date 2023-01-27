from datetime import datetime

from PySide6.QtCore import Qt, QDate, Signal, QEvent, QPoint, QObject
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


class ErrorLabel(QLabel):
    """
    A label that is displayed when the input is invalid.
    The label acts as a tooltip and is displayed above the input.
    The label is hidden when the input is valid, and when the input is not hovered.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlag(Qt.ToolTip)
        self.setVisible(False)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(
            """
            border: 1px solid red;
            background-color: #f8d7da;
            """
        )

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Show:
            qpoint = QPoint(
                self.buddy().rect().center().x(),
                self.buddy().rect().top() - self.height() - 10,
            )
            global_qpoint = self.buddy().mapToGlobal(QPoint(0, 0))
            self.move(qpoint + global_qpoint)

        return super().eventFilter(obj, event)


_mapper = {
    "h1": (H1QLabel, H1QSeparator),
    "h2": (H2QLabel, H1QSeparator),
}


class StyledLabelComponent(QWidget):
    """
    A widget that contains a label and a separator.
    Used as a header for a section.
    """

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


class EditElementSignals(QObject):
    input_changed = Signal()


class EditElementInterface:
    ERROR_STYLES = "border: 1px solid red;"

    signals = EditElementSignals()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.signals = EditElementSignals()

    def valid(self) -> bool:
        return True

    def set_error_state(self):
        pass

    def set_correct_state(self):
        pass

    def is_modified(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError


class NoFrameLineEdit(QLineEdit, EditElementInterface):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setFrame(False)

        self.setObjectName(kwargs.get("object_name", ""))
        self.setPlaceholderText(kwargs.get("placeholder", ""))
        self.setValidator(kwargs.get("validator", None))
        self.setText(kwargs.get("initial_value", None))

        self.textChanged.connect(self.signals.input_changed)

    def valid(self) -> bool:
        return self.hasAcceptableInput()

    def is_modified(self) -> bool:
        return self.isModified()

    def set_error_state(self) -> None:
        self.setStyleSheet(self.ERROR_STYLES)

    def set_correct_state(self) -> None:
        self.setStyleSheet("")

    def value(self):
        return self.text()


class NoFrameDateEdit(QDateEdit, EditElementInterface):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setFrame(False)

        self._is_modified = False

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

        self.dateChanged.connect(self.signals.input_changed)
        self.dateChanged.connect(lambda _: setattr(self, "_is_modified", True))

    def valid(self) -> bool:
        return self.hasAcceptableInput()

    def set_error_state(self) -> None:
        self.setStyleSheet(self.ERROR_STYLES)

    def set_correct_state(self) -> None:
        self.setStyleSheet("")

    def is_modified(self) -> bool:
        return self._is_modified

    def value(self):
        return self.date().toPython()


class ComboBoxEdit(QComboBox, EditElementInterface):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setFrame(False)
        self._is_modified = False

        self.setObjectName(kwargs.get("object_name", ""))
        self.addItems(kwargs.get("items", []))

        self.currentTextChanged.connect(self.signals.input_changed)
        self.currentTextChanged.connect(lambda _: setattr(self, "_is_modified", True))
        self.setCurrentText(kwargs.get("initial_value", None))

    def is_modified(self) -> bool:
        return self._is_modified

    def value(self):
        return self.currentText()