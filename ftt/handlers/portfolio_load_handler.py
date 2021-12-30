from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_load_step import PortfolioLoadStep


class PortfolioLoadHandler(Handler):
    params = ("portfolio_id",)

    handlers = [
        (PortfolioLoadStep, "portfolio_id"),
        (ReturnResult, PortfolioLoadStep.key),
    ]
