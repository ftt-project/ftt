from PySide6.QtWidgets import QWidget, QFormLayout
from ftt.ui.forms.form_element import FormElementBuilder


class Form(QWidget):
    def __init__(self, parent, elements: list = None, layout_class=QFormLayout):
        super().__init__(parent)
        self.setLayout(layout_class())
        self._elements = elements or []

        self.create_ui()

    def add_element(self, element: FormElementBuilder):
        self._elements.append(element)

    def create_ui(self) -> None:
        for element in self._elements:
            element.create_ui(self)

    def validate(self) -> bool:
        return all([element.validate() for element in self._elements])

    def reset(self) -> None:
        for element in self._elements:
            element.reset()
