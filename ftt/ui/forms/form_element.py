from PySide6 import QtGui
from PySide6.QtCore import QPoint, QEvent
from PySide6.QtGui import QValidator, Qt
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QDateEdit
from qtpy import QtCore

from ftt.ui.shared_elements import EditElementInterface


class FormElementBuilder(QWidget):
    def __init__(
        self,
        label=QLabel,
        edit_element=EditElementInterface,
        object_name: str = None,
        validator: QValidator = None,
        placeholder: str = None,
        initial_value=None,
    ):
        super().__init__()
        self._label = label
        self._edit_element = edit_element
        self._initial_value = initial_value
        self._object_name = object_name
        self._validator = validator
        self._placeholder = placeholder

        self._error = ""
        self._error_label = None
        self._error_style = "border: 1px solid red;"

    def create_ui(self, parent: QWidget) -> None:
        parent.layout().addRow(self._label, self._edit_element)
        self._edit_element.inputChanged.connect(self.validate)
        self._edit_element.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self._label.setBuddy(self._edit_element)

        self._error_label = QLabel(parent, Qt.ToolTip)
        self._error_label.setVisible(False)
        parent.layout().addRow("", self._error_label)

        parent.installEventFilter(self)
        self._edit_element.installEventFilter(self)

    def validate(self) -> bool:
        if self._edit_element.hasAcceptableInput():
            self._edit_element.setStyleSheet("")
            self._error_label.setText(self._error)
            self._error_label.setStyleSheet(self._error_style)
            self._error_label.setVisible(False)
            return True
        else:
            self._edit_element.setStyleSheet(self._error_style)
            self._error_label.setText(
                "- Portfolio name must be unique longer than 2 symbols<br>"
                "- Portfolio name must shorter than 30 symbols"
            )
            self._error_label.setStyleSheet("")
            self._error_label.setVisible(True)
            self._error_label.show()
            qpoint = QPoint(
                self._edit_element.x() + self._edit_element.width() / 20,
                self._edit_element.y() - self._error_label.height() - 15,
            )
            global_qpoint = self._edit_element.mapToGlobal(QPoint(0, 0))
            self._error_label.move(qpoint + global_qpoint)
            return False

    def valid(self) -> bool:
        return self._edit_element.valid()

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
        self._edit.clear()
        self._edit.setStyleSheet("")
        self._error_label.setText("")
        self._error_label.setStyleSheet("")
        self._error_label.setVisible(False)
