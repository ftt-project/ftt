from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_steps.portfolio_versions_list_step import (
    PortfolioVersionsListStep,
)


class PortfolioVersionsListHandler(Handler):
    handlers = [
        (PortfolioVersionsListStep, "portfolio"),
        ReturnResult(PortfolioVersionsListStep.key),
    ]
