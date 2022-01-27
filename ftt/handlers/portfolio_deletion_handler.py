from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_load_step import PortfolioLoadStep
from ftt.handlers.portfolio_steps.portfolio_delete_step import PortfolioDeleteStep


class PortfolioDeletionHandler(Handler):
    params = ("portfolio_id",)

    handlers = [
        (PortfolioLoadStep, "portfolio_id"),
        (PortfolioDeleteStep, PortfolioLoadStep.key),
        (ReturnResult, PortfolioDeleteStep.key),
    ]
