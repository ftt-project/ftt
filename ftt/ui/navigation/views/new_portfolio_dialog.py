from enum import Enum
from typing import Union, Any

from PySide6.QtCore import QAbstractTableModel, QPersistentModelIndex, QModelIndex, Slot, QDate
from PySide6.QtGui import QValidator, Qt, QIntValidator
from PySide6.QtWidgets import (
    QDialog,
    QLineEdit,
    QLabel,
    QDialogButtonBox,
    QWidget, QCompleter, QPushButton, QTableView, QHeaderView, QSizePolicy, QFormLayout, QDateEdit,
)
from result import Ok, Err

from ftt.handlers.portfolio_creation_handler import PortfolioCreationHandler
from ftt.ui.model import get_model
from ftt.ui.state import get_state


class PortfolioNameValidator(QValidator):
    def validate(self, text, pos):
        if len(text) < 2:
            return QValidator.Intermediate
        elif len(text) >= 30:
            return QValidator.Invalid
        else:
            return QValidator.Acceptable


class SecuritySymbolValidator(QValidator):
    def validate(self, text, pos):
        if len(text) == 0:
            return QValidator.Intermediate
        elif len(text) >= 10:
            return QValidator.Invalid
        else:
            return QValidator.Acceptable


class SecuritiesModel(QAbstractTableModel):
    class Headers(str, Enum):
        SYMBOL = "Symbol"
        STOCK_EXCHANGE = "Stock Exchange"
        CURRENCY = "Currency"

    def __init__(self, *args, securities=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.securities: list[dict] = securities or []

    def get_securities(self):
        return self.securities

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.DisplayRole:
            return self.securities[index.row()][list(self.Headers)[index.column()].value]
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter

    def insertRow(self, row, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row)
        self.securities.insert(row, {i.value: "" for i in self.Headers})
        self.endInsertRows()
        return True

    def setData(self, index: Union[QModelIndex, QPersistentModelIndex], value: Any, role: int = Qt.EditRole) -> bool:
        if not index.isValid() or role != Qt.EditRole:
            return False

        self.securities[index.row()][list(self.Headers)[index.column()].value] = value
        self.dataChanged.emit(index, index, [role])
        return True

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return list(self.Headers)[section].value
        return super().headerData(section, orientation, role)

    def rowCount(self, index=None):
        return len(self.securities)

    def columnCount(self, parent=QModelIndex()):
        return len(self.Headers)

    def removeRows(self, position, rows, index):
        self.beginRemoveRows(index, position, position + rows - 1)
        for i in range(rows):
            del (self.securities[position])
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True


class SearchSecurityFormElementBuilder(QWidget):
    def __init__(self, model: SecuritiesModel):
        super().__init__()
        self.lookup_confirm_button = None
        self.search_input = None
        self.model = model
        self._state = get_state()
        self.completer = QCompleter(self.model)

    def createUI(self, dialog: QDialog):
        self.search_input = QLineEdit()
        self.search_input.setMinimumWidth(300)
        self.search_input.setObjectName("search_input")
        self.search_input.setCompleter(self.completer)
        self.search_input.setValidator(SecuritySymbolValidator())
        self.search_input.textChanged.connect(self.on_search_input_text_changed)
        dialog.layout().addRow("Security Name", self.search_input)

        self.lookup_confirm_button = QPushButton("Look up and add")
        self.lookup_confirm_button.setObjectName("confirm_button")
        self.lookup_confirm_button.setEnabled(False)
        self.lookup_confirm_button.clicked.connect(self.on_confirm_button_clicked)
        dialog.layout().addRow("", self.lookup_confirm_button)

    def validate(self):
        return self.search_input.hasAcceptableInput()

    @Slot()
    def on_search_input_text_changed(self):
        self.lookup_confirm_button.setEnabled(self.validate())

    @Slot()
    def on_confirm_button_clicked(self):
        last = self.model.rowCount()
        self.model.insertRow(last)
        self.model.setData(self.model.index(last, 0), self.search_input.text())
        self.search_input.clear()

    def reset(self):
        self.search_input.clear()


class SecuritiesTableFormElementBuilder(QWidget):
    def __init__(self, model: SecuritiesModel):
        super().__init__()
        self._state = get_state()
        self.table = None
        self.model = model

    def createUI(self, dialog: QDialog):
        self.table = QTableView()
        self.table.setModel(self.model)

        horizontal_header = self.table.horizontalHeader()
        horizontal_header.setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        horizontal_header.setStretchLastSection(True)

        vertical_header = self.table.verticalHeader()
        vertical_header.setVisible(False)

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        size.setHorizontalStretch(1)
        self.table.setSizePolicy(size)

        dialog.layout().addRow(self.table)

        self._state.signals.selectedPortfolioVersionSecuritiesChanged.connect(
            lambda: self.model.removeRows(0, self.model.rowCount(), QModelIndex())
        )
        self._state.signals.addSecurityDialogClosed.connect(
            lambda: self.model.removeRows(0, self.model.rowCount(), QModelIndex())
        )

    def validate(self):
        return True

    def reset(self):
        self.model.removeRows(0, self.model.rowCount(), QModelIndex())


class PortfolioDetailsFormElementBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.value_field_validation_message = None
        self.value_field = None
        self.name_field_validation_message = None
        self.main_layout = None
        self.name_field = None

    def createUI(self, dialog: QDialog):
        self.name_field = QLineEdit()
        self.name_field.setMinimumWidth(300)
        self.name_field.setObjectName("name_input")
        self.name_field.setValidator(PortfolioNameValidator())
        self.name_field.textChanged.connect(self.name_field_validate)
        dialog.layout().addRow("Portfolio Name", self.name_field)

        self.name_field_validation_message = QLabel(
            "- Portfolio name must be unique longer than 2 symbols<br>"
            "- Portfolio name must shorter than 30 symbols"
        )
        self.name_field_validation_message.setVisible(False)
        dialog.layout().addRow("", self.name_field_validation_message)

        self.value_field = QLineEdit()
        self.name_field.setMinimumWidth(300)
        self.value_field.setObjectName("value_input")
        self.value_field.setValidator(QIntValidator(1, 1000000000))
        self.value_field.setPlaceholderText("$1000")
        self.value_field.textChanged.connect(self.value_field_validate)
        dialog.layout().addRow("Portfolio Value", self.value_field)

        self.value_field_validation_message = QLabel(
            "- Portfolio value must be a number"
        )
        self.value_field_validation_message.setVisible(False)
        dialog.layout().addRow("", self.value_field_validation_message)

    @Slot()
    def name_field_validate(self):
        if self.name_field.hasAcceptableInput():
            self.name_field.setStyleSheet("")
            self.name_field_validation_message.setVisible(False)
            return True
        else:
            self.name_field.setStyleSheet("border: 1px solid red;")
            self.name_field_validation_message.setVisible(True)
            return False

    @Slot()
    def value_field_validate(self):
        if self.value_field.hasAcceptableInput():
            self.value_field.setStyleSheet("")
            self.value_field_validation_message.setVisible(False)
            return True
        else:
            self.value_field.setStyleSheet("border: 1px solid red")
            self.value_field_validation_message.setVisible(True)
            return False

    def validate(self) -> bool:
        return all([
            self.name_field_validate(),
            self.value_field_validate()
        ])

    def reset(self):
        self.name_field.clear()
        self.value_field.clear()
        self.name_field_validation_message.setVisible(False)
        self.value_field_validation_message.setVisible(False)


class PortfolioDateRangeFormElementBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.validation_message = None
        self.main_layout = None
        self.start_date_field = None
        self.end_date_field = None

    def createUI(self, dialog: QDialog):
        self.start_date_field = QDateEdit()
        self.start_date_field.setMinimumWidth(300)
        self.start_date_field.setObjectName("start_date_input")
        self.start_date_field.setCalendarPopup(True)
        self.start_date_field.setDisplayFormat("yyyy-MM-dd")
        self.start_date_field.setDate(QDate.currentDate().addYears(-2))
        self.start_date_field.setMaximumDate(QDate.currentDate())
        self.start_date_field.dateChanged.connect(self.start_date_field_validate)
        dialog.layout().addRow("Start Date", self.start_date_field)

        self.end_date_field = QDateEdit()
        self.end_date_field.setMinimumWidth(300)
        self.end_date_field.setObjectName("end_date_input")
        self.end_date_field.setCalendarPopup(True)
        self.end_date_field.setDisplayFormat("yyyy-MM-dd")
        self.end_date_field.setDate(QDate.currentDate())
        self.end_date_field.setMaximumDate(QDate.currentDate())
        self.end_date_field.dateChanged.connect(self.end_date_field_validate)
        dialog.layout().addRow("End Date", self.end_date_field)

        self.validation_message = QLabel(
            "- Start date must be before end date<br>"
            "- Start date must be before today<br>"
            "- End date must be before today"
        )
        self.validation_message.setVisible(False)
        dialog.layout().addRow("", self.validation_message)

    @Slot()
    def start_date_field_validate(self):
        if self.start_date_field.date() < self.end_date_field.date() and \
                self.start_date_field.date() < QDate.currentDate():
            self.validation_message.setVisible(False)
            self.start_date_field.setStyleSheet("")
            return True
        else:
            self.validation_message.setVisible(True)
            self.start_date_field.setStyleSheet("border: 1px solid red")
            return False

    @Slot()
    def end_date_field_validate(self):
        if self.end_date_field.date() <= QDate.currentDate():
            self.validation_message.setVisible(False)
            self.end_date_field.setStyleSheet("")
            return True
        else:
            self.validation_message.setVisible(True)
            self.end_date_field.setStyleSheet("border: 1px solid red")
            return False

    def validate(self) -> bool:
        return all([
            self.start_date_field_validate(),
            self.end_date_field_validate()
        ])

    def reset(self):
        self.start_date_field.setDate(QDate.currentDate().addYears(-2))
        self.end_date_field.setDate(QDate.currentDate())
        self.validation_message.setVisible(False)


class FormElements:
    def __init__(self, *elements: QWidget):
        self._elements = elements or []
        self.i = len(self._elements) - 1

    def validate(self) -> bool:
        return all([element.validate() for element in self._elements])

    def createUI(self, dialog: QDialog):
        for element in self._elements:
            element.createUI(dialog)

    def reset(self):
        for element in self._elements:
            element.reset()


class NewPortfolioDialog(QDialog):
    def __init__(self):
        super().__init__()

        self._state = get_state()
        self._model = get_model()
        self._securities_model = SecuritiesModel()
        self._hint_message = None
        self._buttons = None
        self._layout = None
        self._form_elements = None
        self.createUI()

    def createUI(self):
        self.setWindowTitle("New Portfolio")
        self._layout = QFormLayout(self)

        self._form_elements = FormElements(
            PortfolioDetailsFormElementBuilder(),
            PortfolioDateRangeFormElementBuilder(),
            SearchSecurityFormElementBuilder(self._securities_model),
            SecuritiesTableFormElementBuilder(self._securities_model),
        )
        self._form_elements.createUI(self)

        self._buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def accept(self) -> None:
        if not self._form_elements.validate():
            return None

        name = self.findChild(QLineEdit, "name_input").text()
        value = self.findChild(QLineEdit, "value_input").text()
        start_date = self.findChild(QDateEdit, "start_date_input").date().toPyDate()
        end_date = self.findChild(QDateEdit, "end_date_input").date().toPyDate()
        securities = self._securities_model.get_securities()
        result = PortfolioCreationHandler().handle(name=name)
        match result:
            case Ok(portfolio):
                self._state.close_new_portfolio_dialog(portfolio.id)
                self._form_elements.reset()
                super().accept()
            case Err():
                self._hint_message.setText(result.unwrap_err())
                self._hint_message.show()

    def reject(self) -> None:
        self._form_elements.reset()
        self._state.close_new_portfolio_dialog(self._model.portfolio_id)
        super().reject()
