from PySide6.QtCore import (
    QModelIndex,
    Slot,
    QDate,
    Qt,
    QItemSelection,
)
from PySide6.QtGui import QValidator, QIntValidator
from PySide6.QtWidgets import (
    QDialog,
    QLineEdit,
    QLabel,
    QDialogButtonBox,
    QWidget,
    QCompleter,
    QPushButton,
    QTableView,
    QHeaderView,
    QSizePolicy,
    QFormLayout,
    QDateEdit,
    QComboBox,
    QToolBar,
    QHBoxLayout,
    QAbstractItemView,
)
from result import Ok, Err
import qtawesome as qta  # type: ignore[import]

from ftt.handlers.portfolio_creation_handler import PortfolioCreationHandler
from ftt.handlers.securities_external_information_upsert_handler import (
    SecuritiesExternalInformationUpsertHandler,
)
from ftt.storage import schemas
from ftt.storage.schemas import ACCEPTABLE_INTERVALS
from ftt.ui.forms.forms import Form
from ftt.ui.model import get_model, CollectionModel
from ftt.ui.state import get_state
from ftt.ui.validators import PortfolioNameValidator, SecuritySymbolValidator
from ftt.ui.workers import SecuritiesInformationLoadingWorker


class SecuritiesModel(CollectionModel):
    """
    Used as an example
    https://github.com/pyside/Examples/blob/master/examples/itemviews/addressbook/tablemodel.py
    https://doc.qt.io/qtforpython-6.2/tutorials/datavisualize/add_tableview.html
    """

    def get_securities(self):
        return self._collection


class SearchSecurityFormElementBuilder(QWidget):
    def __init__(self, model: SecuritiesModel):
        super().__init__()
        self.validation_message = None
        self.lookup_confirm_button = None
        self.search_input = None
        self.model = model
        self._state = get_state()
        self.completer = QCompleter(self.model)

    def create_ui(self, dialog: QDialog):
        self.search_input = QLineEdit()
        self.search_input.setMinimumWidth(300)
        self.search_input.setObjectName("search_input")
        self.search_input.setCompleter(self.completer)
        self.search_input.setValidator(SecuritySymbolValidator())
        self.search_input.textChanged.connect(self.on_search_input_text_changed)
        dialog.layout().addRow("Security Name", self.search_input)

        self.validation_message = QLabel("")
        self.validation_message.setObjectName("validation_message")
        self.validation_message.setVisible(False)
        dialog.layout().addRow("", self.validation_message)

        self.lookup_confirm_button = QPushButton("")
        self.lookup_confirm_button.setText("Look up and add")
        self.lookup_confirm_button.setEnabled(False)
        self.lookup_confirm_button.setObjectName("confirm_button")
        self.lookup_confirm_button.clicked.connect(self.on_confirm_search_event)
        dialog.layout().addRow("", self.lookup_confirm_button)

    def validate(self):
        return True

    def show_validation_message(self, message):
        self.validation_message.setText(message)
        self.validation_message.setVisible(True)
        self.search_input.setStyleSheet("border: 1px solid red;")

    def hide_validation_message(self):
        self.validation_message.setVisible(False)
        self.search_input.setStyleSheet("")

    def search_button_is_loading_mode(self):
        self.search_input.setEnabled(False)
        self.lookup_confirm_button.setText("Loading...")
        self.lookup_confirm_button.setEnabled(False)

    def search_button_is_ready(self):
        self.search_input.setEnabled(True)
        self.lookup_confirm_button.setText("Look up and add")
        self.lookup_confirm_button.setEnabled(True)

    @Slot()
    def on_search_input_text_changed(self):
        self.hide_validation_message()
        self.lookup_confirm_button.setEnabled(self.search_input.hasAcceptableInput())

    @Slot()
    def on_confirm_search_event(self):
        validator = self.search_input.validator()
        state = validator.validate_uniquness(
            self.search_input.text(),
            [record.symbol for record in self.model.get_securities()],
        )
        if state == QValidator.State.Invalid:
            self.show_validation_message(
                "- Symbol must be shorter than 10 characters\n"
                "- Symbol must be unique"
            )
            return

        security = schemas.Security(
            symbol=self.search_input.text(),
        )

        self.search_button_is_loading_mode()
        SecuritiesInformationLoadingWorker.perform(
            [security],
            success_callback=lambda x: self.on_securities_information_loaded(x),
            failure_callback=lambda x: self.on_securities_information_load_error(x),
            complete_callback=lambda: self.search_button_is_ready(),
        )

        self.search_input.clear()

    @Slot()
    def on_securities_information_loaded(self, securities: list[schemas.Security]):
        self.model.add(securities[0])

    @Slot()
    def on_securities_information_load_error(self, error: list[str]):
        self.show_validation_message("".join([f"- {e}" for e in error]))

    def reset(self):
        self.search_input.clear()
        self.search_input.setStyleSheet("")


class SecuritiesTableFormElementBuilder(QWidget):
    def __init__(self, model: SecuritiesModel):
        super().__init__()
        self.remove_action = None
        self._state = get_state()
        self.table = None
        self.model = model

    def create_ui(self, dialog: QDialog):
        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setModel(self.model)
        self.table.selectionModel().selectionChanged.connect(
            lambda selected, deselected: self.on_selection_changed(selected, deselected)
        )

        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setOrientation(Qt.Vertical)
        self.remove_action = QPushButton(qta.icon("ri.delete-bin-2-line"), "")
        self.remove_action.clicked.connect(self.remove_selected_securities)
        self.remove_action.setEnabled(False)
        toolbar.addWidget(self.remove_action)

        horizontal_header = self.table.horizontalHeader()
        horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        horizontal_header.setStretchLastSection(True)

        vertical_header = self.table.verticalHeader()
        vertical_header.setVisible(False)

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        size.setHorizontalStretch(1)
        self.table.setSizePolicy(size)

        w = QWidget()
        w.setLayout(QHBoxLayout())
        w.layout().addWidget(self.table)
        w.layout().addWidget(toolbar)
        dialog.layout().addRow(w)

        self._state.signals.selectedPortfolioVersionSecuritiesChanged.connect(
            lambda: self.model.clear()
        )
        self._state.signals.addSecurityDialogClosed.connect(lambda: self.model.clear())

    def validate(self):
        return True

    def reset(self):
        self.model.removeRows(0, self.model.rowCount(), QModelIndex())

    def on_selection_changed(self, selected: QItemSelection, _):
        if selected.count() > 0:
            self.remove_action.setEnabled(True)
        else:
            self.remove_action.setEnabled(False)

    def remove_selected_securities(self):
        selected_rows = self.table.selectionModel().selectedRows()
        for row in selected_rows:
            self.model.removeRows(row.row())


class PortfolioDetailsFormElementBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.value_field_validation_message = None
        self.value_field = None
        self.name_field_validation_message = None
        self.main_layout = None
        self.name_field = None

    def create_ui(self, dialog: QDialog):
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
        return all([self.name_field_validate(), self.value_field_validate()])

    def reset(self):
        self.name_field.clear()
        self.name_field.setStyleSheet("")
        self.value_field.clear()
        self.value_field.setStyleSheet("")
        self.name_field_validation_message.setVisible(False)
        self.value_field_validation_message.setVisible(False)


class PortfolioDateRangeFormElementBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.interval_field = None
        self.validation_message = None
        self.main_layout = None
        self.start_date_field = None
        self.end_date_field = None

    def create_ui(self, dialog: QDialog):
        self.interval_field = QComboBox()
        self.interval_field.setObjectName("interval_input")
        self.interval_field.addItems(ACCEPTABLE_INTERVALS)
        dialog.layout().addRow("Interval", self.interval_field)

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
        if (
            self.start_date_field.date() < self.end_date_field.date()
            and self.start_date_field.date() < QDate.currentDate()
        ):
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
        return all([self.start_date_field_validate(), self.end_date_field_validate()])

    def reset(self):
        self.start_date_field.setDate(QDate.currentDate().addYears(-2))
        self.start_date_field.setStyleSheet("")
        self.end_date_field.setDate(QDate.currentDate())
        self.end_date_field.setStyleSheet("")
        self.validation_message.setVisible(False)


class NewPortfolioDialog(QDialog):
    def __init__(self):
        super().__init__()

        self._state = get_state()
        self._model = get_model()
        self._securities_model = SecuritiesModel(
            collection=[],
            headers={
                "symbol": "Symbol",
                "currency": "Currency",
                "exchange": "Stock Exchange",
            },
        )
        self._hint_message = None
        self._buttons = None
        self._layout = None
        self._form_elements = None
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("New Portfolio")
        self._layout = QFormLayout(self)
        return

        self._form_elements = Form(
            PortfolioDetailsFormElementBuilder(),
            PortfolioDateRangeFormElementBuilder(),
            SearchSecurityFormElementBuilder(self._securities_model),
            SecuritiesTableFormElementBuilder(self._securities_model),
        )
        self._form_elements.create_ui(self)

        self._layout.addRow("", self._hint_message)
        self._buttons = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Save
        )
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def accept(self) -> None:
        if not self._form_elements.validate():
            return None

        securities_upsert_result = SecuritiesExternalInformationUpsertHandler().handle(
            securities=self._securities_model.get_securities()
        )
        match securities_upsert_result:
            case Err(error):
                self._hint_message.setText(error.unwrap_error())
                self._hint_message.show()
                return None

        portfolio = schemas.Portfolio(
            name=self.findChild(QLineEdit, "name_input").text(),
            value=self.findChild(QLineEdit, "value_input").text(),
            period_start=self.findChild(QDateEdit, "start_date_input")
            .date()
            .toPython(),
            period_end=self.findChild(QDateEdit, "end_date_input").date().toPython(),
            interval=self.findChild(QComboBox, "interval_input").currentText(),
            securities=[],
        )

        result = PortfolioCreationHandler().handle(
            portfolio=portfolio, securities=securities_upsert_result.unwrap()
        )
        match result:
            case Ok(portfolio):
                self._state.confirm_new_portfolio_dialog(portfolio.id)
                self._form_elements.reset()
                super().accept()
            case Err():
                self._hint_message.setText(result.unwrap_err())
                self._hint_message.show()

    def reject(self) -> None:
        self._form_elements.reset()
        self._state.close_new_portfolio_dialog(self._model.portfolio_id)
        super().reject()
