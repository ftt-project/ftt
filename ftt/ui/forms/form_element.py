from PySide6.QtCore import QEvent
from PySide6.QtGui import QValidator, Qt
from PySide6.QtWidgets import QWidget, QLabel

from ftt.ui.shared_elements import EditElementInterface, ErrorLabel


class FormElement(QWidget):
    def __init__(
        self,
        label=QLabel,
        edit_element=EditElementInterface,
        object_name: str = None,
        validator: QValidator = None,
        placeholder: str = None,
        initial_value=None,
        error_message: str = None,
    ):
        super().__init__()
        self._label = label
        self._edit_element = edit_element
        self._initial_value = initial_value
        self._object_name = object_name
        self._validator = validator
        self._placeholder = placeholder

        self._error_message = error_message
        self._error_label = None

    def create_ui(self, parent: QWidget) -> None:
        parent.layout().addRow(self._label, self._edit_element)
        self._edit_element.signals.input_changed.connect(self.validate)
        self._edit_element.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self._label.setBuddy(self._edit_element)

        self._error_label = ErrorLabel(parent)
        self._error_label.setText(self._error_message)
        self._error_label.setBuddy(self._edit_element)
        parent.layout().addWidget(self._error_label)
        parent.layout().setRowVisible(self._error_label, False)

        self._edit_element.installEventFilter(self)

    def validate(self) -> bool:
        if self._edit_element.valid():
            self._edit_element.set_correct_state()
            self._error_label.hide()
            return True
        else:
            self._edit_element.set_error_state()
            self._error_label.show()
            return False

    def valid(self) -> bool:
        return self._edit_element.valid()

    def is_modified(self) -> bool:
        return self._edit_element.is_modified()

    def eventFilter(self, obj, event):
        if obj == self._edit_element:
            match event.type():
                case QEvent.Type.FocusIn | QEvent.Type.HoverEnter:
                    if not self.valid():
                        self._error_label.show()
                case QEvent.Type.FocusOut | QEvent.Type.HoverLeave:
                    self._error_label.hide()

        return super().eventFilter(obj, event)

    def reset(self):
        self._edit_element.clear()
        self._edit_element.setStyleSheet("")
        self._error_label.setText("")
        self._error_label.setStyleSheet("")
        self._error_label.setVisible(False)

    def on_change(self, callback):
        self._edit_element.signals.input_changed.connect(callback)
