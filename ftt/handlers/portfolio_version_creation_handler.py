from ftt.handlers.handler.context import Context
from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_version_create_step import (
    PortfolioVersionCreateStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_next_version_calculation_step import (
    PortfolioVersionNextVersionCalculationStep,
)


class PortfolioVersionCreationHandler(Handler):
    params = ("portfolio", "value", "period_start", "period_end", "interval")

    handlers = [
        (PortfolioVersionNextVersionCalculationStep, "portfolio"),
        Context(rename=PortfolioVersionNextVersionCalculationStep.key, to="version"),
        (
            PortfolioVersionCreateStep,
            "portfolio",
            "version",
            "value",
            "period_start",
            "period_end",
            "interval",
        ),
        (ReturnResult, PortfolioVersionCreateStep.key),
    ]
