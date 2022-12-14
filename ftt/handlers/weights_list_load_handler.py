from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.weights_steps.weights_load_step import WeightsLoadStep
from ftt.storage import schemas


class WeightsListLoadHandler(Handler):
    params = {"portfolio_version": schemas.PortfolioVersion}

    handlers = [
        (WeightsLoadStep, "portfolio_version"),
        (ReturnResult, WeightsLoadStep.key),
    ]
