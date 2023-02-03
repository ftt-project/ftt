from datetime import datetime
from typing import Optional, cast

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QWidget, QFormLayout, QDialogButtonBox
from ftt.ui.forms.form_element import FormElement
from ftt.ui.shared_elements import EditElementInterface


class FormSignals(QObject):
    on_accept = Signal()
    on_reject = Signal()


class Form(QWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        elements: Optional[list] = None,
        layout_class=QFormLayout,
    ):
        super().__init__(parent)
        self.setLayout(layout_class())
        self._elements = elements or []

        self.signals = FormSignals()

        self._buttons_box = QDialogButtonBox()
        self._buttons_box.addButton("Reset", QDialogButtonBox.ButtonRole.RejectRole)
        self._buttons_box.addButton("Apply", QDialogButtonBox.ButtonRole.AcceptRole)

    def add_element(self, element: FormElement):
        element.create_ui(self)
        self._elements.append(element)

    def set_element_value(self, name: str, value: str | datetime) -> None:
        widget = cast(EditElementInterface, self.findChild(QWidget, name))
        widget.set_value(value)

    def get_element_value(self, name: str) -> str | datetime:
        widget = cast(EditElementInterface, self.findChild(QWidget, name))
        return widget.value()

    def create_ui(self) -> None:
        for element in self._elements:
            element.create_ui(self)

        for element in self._elements:
            element.on_change(lambda *args, el=element: self._on_change(args, el))

        # for button in self._buttons_box.buttons():
        #     button.setEnabled(False)
        self.layout().addWidget(self._buttons_box)

        self._buttons_box.accepted.connect(self._on_accept)  # type: ignore[attr-defined]
        self._buttons_box.accepted.connect(self.signals.on_accept)  # type: ignore[attr-defined]
        self._buttons_box.rejected.connect(self._on_reject)  # type: ignore[attr-defined]
        self._buttons_box.rejected.connect(self.signals.on_reject)  # type: ignore[attr-defined]

    def validate(self) -> bool:
        return all([element.validate() for element in self._elements])

    def reset(self) -> None:
        for element in self._elements:
            element.reset()

    def _on_change(self, args: str, element: FormElement) -> None:
        pass

    def _enable_buttons(self) -> None:
        for button in self._buttons_box.buttons():
            button.setEnabled(True)

    def _disable_buttons(self) -> None:
        for button in self._buttons_box.buttons():
            button.setEnabled(False)

    def _on_accept(self) -> None:
        pass

    def _on_reject(self) -> None:
        self.reset()
        self._disable_buttons()
