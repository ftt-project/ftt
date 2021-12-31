from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_versions_list_step import (
    PortfolioVersionsListStep,
)


class PortfolioVersionsListHandler(Handler):
    """
    Returns a list of all versions of a portfolio.
    """

    params = ("portfolio",)

    handlers = [
        (PortfolioVersionsListStep, "portfolio"),
        (ReturnResult, PortfolioVersionsListStep.key),
    ]
