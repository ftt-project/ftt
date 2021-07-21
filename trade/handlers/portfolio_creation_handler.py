from trade.handlers.handler.context import Context
from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_steps.portfolio_create_step import PortfolioCreateStep
from trade.handlers.portfolio_steps.portfolio_version_create_step import (
    PortfolioVersionCreateStep,
)


class PortfolioCreationHandler(Handler):
    handlers = [
        (PortfolioCreateStep, "name", "amount", "period_start", "period_end", "interval"),
        Context(assign=1, to="version"),
        (PortfolioVersionCreateStep, "version", "portfolio"),
        # (PortfolioAssociateWeightsStep, PortfolioVersionCreateStep.key, "securities"),
        ReturnResult(PortfolioCreateStep.key),
    ]
