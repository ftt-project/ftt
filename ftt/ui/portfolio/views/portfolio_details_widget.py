from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QTableView,
    QAbstractItemView,
    QHeaderView,
    QSizePolicy,
    QVBoxLayout,
    QLineEdit,
    QDateEdit,
)

from ftt.handlers.portfolio_handlers import PortfolioLoadHandler
from ftt.handlers.securities_handler import PortfolioSecuritiesLoadHandler
from ftt.storage import schemas
from ftt.storage.schemas import ACCEPTABLE_INTERVALS
from ftt.ui.forms.form_element import FormElementBuilder
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
        horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        horizontal_header.setStretchLastSection(True)

        vertical_header = self.verticalHeader()
        vertical_header.setVisible(False)

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
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
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self._state = get_state()
        self._model = get_model()
        self.setFixedHeight(250)
        # self.setFixedWidth(400)
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

        self.create_ui()

    def create_ui(self):
        self._state.signals.selectedPortfolioChanged.connect(
            self.display_portfolio_details
        )

    def display_portfolio_details(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()

        result = PortfolioLoadHandler().handle(
            portfolio=schemas.Portfolio(id=self._model.portfolio_id)
        )
        if result.is_err():
            print(result.err())
            return

        form = Form(self)
        form.setFixedWidth(400)
        form.add_element(
            FormElementBuilder(
                label=QLabel("Portfolio name"),
                edit_element=NoFrameLineEdit(
                    object_name="portfolio-name",
                    validator=PortfolioNameValidator(),
                    placeholder="Portfolio name",
                    initial_value=result.unwrap().name,
                ),
            )
        )
        form.add_element(
            FormElementBuilder(
                label=QLabel("Portfolio value"),
                edit_element=NoFrameLineEdit(
                    object_name="portfolio-value",
                    validator=QDoubleValidator(1.0, 1000000000.0, 2),
                    placeholder="$000.00",
                    initial_value=str(result.unwrap().value),
                ),
            )
        )
        form.add_element(
            FormElementBuilder(
                label=QLabel("Period start"),
                edit_element=NoFrameDateEdit(
                    initial_value=result.unwrap().period_start,
                ),
            )
        )
        form.add_element(
            FormElementBuilder(
                label=QLabel("Period end"),
                edit_element=NoFrameDateEdit(
                    initial_value=result.unwrap().period_end,
                ),
            )
        )
        form.add_element(
            FormElementBuilder(
                label=QLabel("Interval"),
                edit_element=ComboBoxEdit(
                    items=ACCEPTABLE_INTERVALS,
                    initial_value=result.unwrap().interval,
                    object_name="portfolio-interval",
                ),
            ),
        )
        form.create_ui()
        self.layout().addWidget(form)


class PortfolioDetailsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout(self)
        self._state = get_state()
        self._model = get_model()

        self.create_ui()

    def create_ui(self):
        self.layout().addWidget(DetailsElementWidget(self))
        # self.layout().addWidget(SecuritiesElementWidget())
        self._layout.addStretch(1)
