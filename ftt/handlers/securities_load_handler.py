from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.securities_steps.securities_load_step import SecuritiesLoadStep


class SecuritiesLoadHandler(Handler):
    params = ("security_symbols",)

    handlers = [
        (SecuritiesLoadStep, "security_symbols"),
        (ReturnResult, SecuritiesLoadStep.key),
    ]
