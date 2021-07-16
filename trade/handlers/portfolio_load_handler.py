from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_steps.portfolio_load_step import PortfolioLoadStep


class PortfolioLoadHandler(Handler):
    handlers = [
        (PortfolioLoadStep, "portfolio_id"),
        ReturnResult(PortfolioLoadStep.key),
    ]
