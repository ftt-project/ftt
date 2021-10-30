from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.weights_steps.weights_load_step import WeightsLoadStep


class WeightsListHandler(Handler):
    handlers = [
        (WeightsLoadStep, "portfolio_version"),
        (ReturnResult, WeightsLoadStep.key),
    ]
