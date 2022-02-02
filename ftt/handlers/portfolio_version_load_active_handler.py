from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_load_step import PortfolioLoadStep
from ftt.handlers.portfolio_version_steps.portfolio_version_load_active_step import (
    PortfolioVersionLoadActiveStep,
)


class PortfolioVersionLoadActiveHandler(Handler):
    params = ("portfolio_id",)

    handlers = [
        (PortfolioLoadStep, "portfolio_id"),
        (PortfolioVersionLoadActiveStep, PortfolioLoadStep.key),
        (ReturnResult, PortfolioVersionLoadActiveStep.key),
    ]
