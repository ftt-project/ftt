from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)


class PortfolioVersionLoadHandler(Handler):
    """
    Loads portfolio version by ID
    """

    params = ("portfolio_version_id",)

    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        (ReturnResult, PortfolioVersionLoadStep.key),
    ]
