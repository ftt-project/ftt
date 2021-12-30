from ftt.handlers.handler.context import Context
from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_create_step import PortfolioCreateStep
from ftt.handlers.portfolio_steps.portfolio_version_create_step import (
    PortfolioVersionCreateStep,
)


class PortfolioCreationHandler(Handler):
    params = ("name", "value", "period_start", "period_end", "interval")

    handlers = [
        (PortfolioCreateStep, "name"),
        Context(assign=1, to="version"),
        (
            PortfolioVersionCreateStep,
            "version",
            "portfolio",
            "value",
            "period_start",
            "period_end",
            "interval",
        ),
        (ReturnResult, PortfolioCreateStep.key),
    ]
