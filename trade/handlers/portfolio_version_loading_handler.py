from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_version_steps.portfolio_version_load_step import PortfolioVersionLoadStep


class PortfolioVersionLoadHandler(Handler):
    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        ReturnResult(PortfolioVersionLoadStep.key)
    ]