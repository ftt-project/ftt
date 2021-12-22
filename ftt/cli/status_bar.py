from nubia import context, statusbar  # type: ignore
from pygments.token import Token  # type: ignore


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

        return [
            t
            for t in [
                (Token.Toolbar, "Verbose "),
                spacer,
                is_verbose,
                spacer,
            ]
            if t is not None
        ]
