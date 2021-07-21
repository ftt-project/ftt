from nubia import context, statusbar
from pygments.token import Name, Token


class StatusBar(statusbar.StatusBar):
    def __init__(self, context):
        self._last_status = None

    def get_rprompt_tokens(self):
        if self._last_status:
            return [(Token.RPrompt, "Error: {}".format(self._last_status))]
        return []

    def set_last_command_status(self, status):
        self._last_status = status

    def get_tokens(self):
        spacer = (Token.Spacer, "  ")
        if context.get_context().verbose:
            is_verbose = (Token.Warn, "ON")
        else:
            is_verbose = (Token.Info, "OFF")

        if context.get_context().portfolio_in_use is not None:
            portfolio = (
                Name.Query,
                f"Active Portfolio #{context.get_context().portfolio_in_use}",
            )
        else:
            portfolio = None

        return [
            t
            for t in [
                (Token.Toolbar, "Verbose "),
                spacer,
                is_verbose,
                spacer,
                portfolio,
            ]
            if t is not None
        ]
