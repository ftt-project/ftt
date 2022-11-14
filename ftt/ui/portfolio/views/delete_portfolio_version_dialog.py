from PySide6.QtWidgets import QDialogButtonBox, QDialog, QVBoxLayout, QLabel
from result import Ok, Err

from ftt.handlers.portfolio_version_deletion_handler import PortfolioVersionDeletionHandler
from ftt.ui.model import get_model
from ftt.ui.state import get_state


class DeletePortfolioVersionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self._layout = None
        self._model = get_model()
        self._state = get_state()
        self.createUI()

    def createUI(self):
        self.setWindowTitle("Confirm Portfolio Version deletion")
        if (
            self._model.portfolio_version_id
            and len(self._model.portfolio_version_id) > 1
        ):
            prompt_text = f"Are you sure you want to delete {len(self._model.portfolio_version_id)} portfolio versions?"
        else:
            prompt_text = "Are you sure you want to delete this portfolio version?"

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._layout.addWidget(QLabel(prompt_text))

        buttons = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self._layout.addWidget(buttons)

    def accept(self) -> None:
        result = PortfolioVersionDeletionHandler().handle(portfolio_version_id=self._model.portfolio_version_id)
        match result:
            case Ok(_):
                self._state.confirm_delete_portfolio_version_dialog()
                super().accept()
            case Err(value):
                print(value)

    def reject(self) -> None:
        self._state.close_delete_portfolio_version_dialog()
        super().reject()
