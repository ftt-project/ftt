from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_load_step import PortfolioLoadStep
from ftt.handlers.portfolio_version_steps.portfolio_version_load_active_step import (
    PortfolioVersionLoadActiveStep,
)
from ftt.storage import schemas


class PortfolioVersionLoadActiveHandler(Handler):
    params = {"portfolio": schemas.Portfolio}

    handlers = [
        (PortfolioLoadStep, "portfolio"),
        (PortfolioVersionLoadActiveStep, PortfolioLoadStep.key),
        (ReturnResult, PortfolioVersionLoadActiveStep.key),
    ]
