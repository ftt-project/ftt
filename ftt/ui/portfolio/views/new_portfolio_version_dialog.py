from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QDateTimeEdit,
    QLineEdit,
    QComboBox,
)
from result import Ok, Err

from ftt.handlers.portfolio_version_creation_handler import (
    PortfolioVersionCreationHandler,
)
from ftt.portfolio_management.optimization_strategies import (
    OptimizationStrategyResolver,
)
from ftt.storage.models.portfolio_version import ACCEPTABLE_INTERVALS
from ftt.ui.model import get_model
from ftt.ui.portfolio.data import getPortfolio
from ftt.ui.state import get_state


class NewVersionFormFields:
    def __init__(self):
        self.value_input = QLineEdit()
        self.period_from_input = QDateTimeEdit()
        self.period_to_input = QDateTimeEdit()

        self.interval_input = QComboBox()
        self.interval_input.addItems(ACCEPTABLE_INTERVALS)

        self.strategy_input = QComboBox()
        self.strategy_input.addItems(OptimizationStrategyResolver.strategies())


class NewPortfolioVersionDialogSignals(QObject):
    newPortfolioVersionCreated = Signal(int)


class NewPortfolioVersionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self._model = get_model()
        self._state = get_state()
        self._buttons = None
        self._layout = None
        self.signals = NewPortfolioVersionDialogSignals()
        self._form_fields = NewVersionFormFields()
        self.createUI()

    def createUI(self):
        self.setWindowTitle("New Portfolio Version")
        self._layout = QFormLayout()
        self.setLayout(self._layout)

        self._layout.addRow("Value", self._form_fields.value_input)
        self._layout.addRow("Period Start", self._form_fields.period_from_input)
        self._layout.addRow("Period End", self._form_fields.period_to_input)
        self._layout.addRow("Interval", self._form_fields.interval_input)
        self._layout.addRow("Optimization Strategy", self._form_fields.strategy_input)

        self._buttons = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.Cancel)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def accept(self) -> None:
        # TODO: self._form_fields.strategy_input is not saved
        # TODO: reset fields after creation
        result = PortfolioVersionCreationHandler().handle(
            portfolio=getPortfolio(self._model.portfolio_id),
            value=int(self._form_fields.value_input.text()),
            interval=self._form_fields.interval_input.currentText(),
            period_start=str(self._form_fields.period_from_input.dateTime().toPython()),
            period_end=str(self._form_fields.period_to_input.dateTime().toPython()),
        )
        match result:
            case Ok(version):
                self._state.close_new_portfolio_version_dialog(version.id)
                super().accept()
            case Err(value):
                print(value)

    def reject(self) -> None:
        self._state.close_new_portfolio_version_dialog(self._model.portfolio_version_id)
        super().reject()
