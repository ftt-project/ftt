from transitions.extensions.nesting import HierarchicalMachine, NestedState

from ftt.ui.model import get_model
from ftt.ui.signals import ApplicationSignals


NestedState.separator = "."


state = None


def get_state():
    global state
    if state is None:
        state = ApplicationState()
    return state


portfolio_screen_configurations = {
    "name": "portfolio_screen",
    "states": ["portfolio_version_selected", "portfolio_version_unselected", "new_portfolio_version_screen",
               "remove_portfolio_version_screen"],
    "transitions": [
        {
            "trigger": "select_portfolio_version",
            "source": "portfolio_version_unselected",
            "dest": "portfolio_version_selected",
            "after": "emit_portfolio_version_selected_signal",
        },
        {
            "trigger": "select_portfolio_version",
            "source": "portfolio_version_selected",
            "dest": "=",
            "after": "emit_portfolio_version_selected_signal",
        },
        {
            "trigger": "unselect_portfolio_version",
            "source": "portfolio_version_selected",
            "dest": "portfolio_version_unselected",
            "after": "emit_portfolio_version_unselected_signal",
        },
        {
            "trigger": "display_new_portfolio_version_dialog",
            "source": ["portfolio_version_selected", "portfolio_version_unselected"],
            "dest": "new_portfolio_version_screen",
            "after": "emit_new_portfolio_version_dialog_displayed_signal",
        },
        {
            "trigger": "close_new_portfolio_version_dialog",
            "source": "new_portfolio_version_screen",
            "dest": "portfolio_version_selected",
            "after": "emit_portfolio_version_selected_signal",
        },
        {
            "trigger": "display_remove_portfolio_version_dialog",
            "source": "portfolio_version_selected",
            "dest": "remove_portfolio_version_screen",
        }
    ],
    "initial": "portfolio_version_unselected",
}

application_states_configuration = {
    "name": "ApplicationState",
    "states": [
        "welcome_screen",
        portfolio_screen_configurations,
        "new_portfolio_screen",
    ],
    "transitions": [
        {
            "trigger": "display_portfolio",
            "source": "welcome_screen",
            "dest": "portfolio_screen",
            "after": "emit_portfolio_selected_signal",
        },
        {
            "trigger": "display_portfolio",
            "source": "portfolio_screen.portfolio_version_unselected",
            "dest": "=",
            "after": "emit_portfolio_selected_signal",
        },
        {
            "trigger": "display_portfolio",
            "source": "portfolio_screen.portfolio_version_selected",
            "dest": "=",
            "after": "emit_portfolio_selected_signal",
        },
        {
            "trigger": "display_new_portfolio_dialog",
            "source": "*",
            "dest": "new_portfolio_screen",
            "after": "emit_new_portfolio_dialog_displayed_signal",
        },
        {
            "trigger": "close_new_portfolio_dialog",
            "source": "new_portfolio_screen",
            "dest": "portfolio_screen",
            "after": "emit_portfolio_selected_signal",
        },
    ],
    "initial": "welcome_screen",
}


class ApplicationState:
    def __init__(self):
        self.signals = ApplicationSignals()
        self.model = get_model()
        self.machine = HierarchicalMachine(
            **application_states_configuration, model=self
        )

    def emit_portfolio_selected_signal(self, portfolio_id):
        self.model.portfolio_id = portfolio_id
        self.signals.selectedPortfolioChanged.emit(portfolio_id)
        self.model.portfolio_version_id = None
        self.signals.selectedPortfolioVersionChanged.emit(None)

    def emit_portfolio_version_selected_signal(self, portfolio_version_id):
        self.model.portfolio_version_id = portfolio_version_id
        self.signals.selectedPortfolioVersionChanged.emit(portfolio_version_id)

    def emit_portfolio_version_unselected_signal(self):
        self.model.portfolio_version_id = None
        self.signals.selectedPortfolioVersionChanged.emit(None)

    def emit_new_portfolio_dialog_displayed_signal(self):
        self.signals.newPortfolioDialogDisplayed.emit()

    def emit_new_portfolio_version_dialog_displayed_signal(self):
        self.signals.newPortfolioVersionDialogDisplayed.emit()
