from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QComboBox,
)
from result import Ok, Err

from ftt.handlers.portfolio_version_creation_handler import (
    PortfolioVersionCreationHandler,
)
from ftt.portfolio_management.allocation_strategies import AllocationStrategyResolver
from ftt.portfolio_management.optimization_strategies import (
    OptimizationStrategyResolver,
)
from ftt.storage import schemas
from ftt.ui.model import get_model
from ftt.ui.state import get_state


class NewVersionFormFields:
    def __init__(self):
        self.optimization_strategy_input = QComboBox()
        self.optimization_strategy_input.addItems(
            OptimizationStrategyResolver.strategies()
        )
        self.allocation_strategy_input = QComboBox()
        self.allocation_strategy_input.addItems(AllocationStrategyResolver.strategies())


class NewPortfolioVersionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self._model = get_model()
        self._state = get_state()
        self._buttons = None
        self._layout = None
        self._form_fields = NewVersionFormFields()
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("New Portfolio Version")
        self._layout = QFormLayout()
        self.setLayout(self._layout)

        self._layout.addRow(
            "Optimization Strategy", self._form_fields.optimization_strategy_input
        )
        self._layout.addRow(
            "Allocation Strategy", self._form_fields.allocation_strategy_input
        )

        self._buttons = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.Cancel)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def accept(self) -> None:
        # TODO: self._form_fields.strategy_input is not saved
        # TODO: reset fields after creation
        result = PortfolioVersionCreationHandler().handle(
            portfolio_version=schemas.PortfolioVersion(
                portfolio=schemas.Portfolio(id=self._model.portfolio_id),
                optimization_strategy_name=self._form_fields.optimization_strategy_input.currentText(),
                allocation_strategy_name=self._form_fields.allocation_strategy_input.currentText(),
            )
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
