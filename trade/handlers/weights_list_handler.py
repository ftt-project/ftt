from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.weights_steps.weights_load_step import WeightsLoadStep


class WeightsListHandler(Handler):
    handlers = [
        (WeightsLoadStep, "portfolio_version"),
        ReturnResult(WeightsLoadStep.key),
    ]
