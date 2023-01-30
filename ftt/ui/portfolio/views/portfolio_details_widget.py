from typing import Optional

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QTableView,
    QAbstractItemView,
    QHeaderView,
    QSizePolicy,
    QVBoxLayout,
)
from result import Err

from ftt.handlers.portfolio_handlers import PortfolioLoadHandler, PortfolioUpdateHandler
from ftt.handlers.securities_handler import PortfolioSecuritiesLoadHandler
from ftt.storage import schemas
from ftt.storage.schemas import ACCEPTABLE_INTERVALS
from ftt.ui.forms.form_element import FormElement
from ftt.ui.forms.forms import Form
from ftt.ui.model import get_model, CollectionModel
from ftt.ui.shared_elements import (
    LabelBuilder,
    NoFrameLineEdit,
    NoFrameDateEdit,
    ComboBoxEdit,
)
from ftt.ui.state import get_state
from ftt.ui.validators import PortfolioNameValidator


class SecuritiesModel(CollectionModel):
    pass


class SecuritiesTable(QTableView):
    def __init__(self, model: SecuritiesModel):
        super().__init__()

        self._model = model
        self.setModel(self._model)

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        horizontal_header = self.horizontalHeader()
        horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        horizontal_header.setStretchLastSection(True)

        vertical_header = self.verticalHeader()
        vertical_header.setVisible(False)

        size = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        size.setHorizontalStretch(1)
        self.setSizePolicy(size)


class SecuritiesElementWidget(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__()
        self.setParent(parent)
        self._layout = QVBoxLayout(self)
        self._securities_model = SecuritiesModel(
            collection=[],
            headers={
                "symbol": "Symbol",
                "quote_type": "Quote type",
                "sector": "Sector",
                "country": "Country",
                "industry": "Industry",
                "currency": "Currency",
                "exchange": "Stock Exchange",
                "short_name": "Short name",
                "long_name": "Long name",
            },
        )
        self._state = get_state()
        self._model = get_model()

        self.create_ui()

    def create_ui(self):
        self._layout.addWidget(
            LabelBuilder.h2_build("Securities"), alignment=Qt.AlignTop
        )

        table = SecuritiesTable(self._securities_model)
        self._layout.addWidget(table)

        self._state.signals.selectedPortfolioChanged.connect(self.display_securities)

        self.parent().layout().addWidget(self)

    def display_securities(self):
        result = PortfolioSecuritiesLoadHandler().handle(
            portfolio=schemas.Portfolio(id=self._model.portfolio_id)
        )

        if result.is_err():
            print(result.err())
            return

        self._securities_model.clear()
        for security in result.unwrap():
            self._securities_model.add(security)


class DetailsElementWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self._state = get_state()
        self._model = get_model()
        self.setFixedHeight(250)
        self.setObjectName("portfolio-details")
        self.setStyleSheet(
            """
            QWidget#portfolio-details {
                margin: 20px 0px;
            }
            QLabel {
                min-width: 100px;
            }
            """
        )
        self.form = Form()

        self.create_ui()

    def create_ui(self):
        self.form.setFixedWidth(400)
        self.form.add_element(
            FormElement(
                label=QLabel("Portfolio name"),
                edit_element=NoFrameLineEdit(
                    object_name="portfolio-name",
                    validator=PortfolioNameValidator(),
                    placeholder="Portfolio name",
                ),
                error_message="- Portfolio name must be unique longer than 2 symbols<br>"
                "- Portfolio name must shorter than 30 symbols",
            )
        )
        self.form.add_element(
            FormElement(
                label=QLabel("Portfolio value"),
                edit_element=NoFrameLineEdit(
                    object_name="portfolio-value",
                    validator=QDoubleValidator(1.0, 1000000000.0, 2),
                    placeholder="$000.00",
                ),
                error_message="- Portfolio value must be a number",
            )
        )
        self.form.add_element(
            FormElement(
                label=QLabel("Period start"),
                edit_element=NoFrameDateEdit(
                    object_name="portfolio-period-start",
                ),
            )
        )
        self.form.add_element(
            FormElement(
                label=QLabel("Period end"),
                edit_element=NoFrameDateEdit(
                    object_name="portfolio-period-end",
                ),
            )
        )
        self.form.add_element(
            FormElement(
                label=QLabel("Interval"),
                edit_element=ComboBoxEdit(
                    object_name="portfolio-interval",
                    items=ACCEPTABLE_INTERVALS,
                ),
            ),
        )
        self.form.create_ui()
        self.form.signals.on_accept.connect(self.update_portfolio)
        self.layout().addWidget(self.form)

        self._state.signals.selectedPortfolioChanged.connect(
            self.display_portfolio_details
        )

    def display_portfolio_details(self):
        result = PortfolioLoadHandler().handle(
            portfolio=schemas.Portfolio(id=self._model.portfolio_id)
        )
        if result.is_err():
            print(result.err())
            return

        self.form.set_element_value("portfolio-name", result.unwrap().name)
        self.form.set_element_value("portfolio-value", str(result.unwrap().value))
        self.form.set_element_value(
            "portfolio-period-start", result.unwrap().period_start
        )
        self.form.set_element_value("portfolio-period-end", result.unwrap().period_end)
        self.form.set_element_value("portfolio-interval", result.unwrap().interval)

    @Slot()
    def update_portfolio(self):
        portfolio = schemas.Portfolio(
            id=self._model.portfolio_id,
            name=self.form.get_element_value("portfolio-name"),
            value=self.form.get_element_value("portfolio-value"),
            period_start=self.form.get_element_value("portfolio-period-start"),
            period_end=self.form.get_element_value("portfolio-period-end"),
            interval=self.form.get_element_value("portfolio-interval"),
            securities=[],
        )
        result = PortfolioUpdateHandler().handle(portfolio=portfolio)

        match result:
            case Err(e):
                print(e)


class PortfolioDetailsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout(self)
        self._state = get_state()
        self._model = get_model()

        self.create_ui()

    def create_ui(self):
        self.layout().addWidget(DetailsElementWidget(self))
        self.layout().addWidget(SecuritiesElementWidget(self))
        self._layout.addStretch(1)
