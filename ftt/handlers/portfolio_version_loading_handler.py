from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)


class PortfolioVersionLoadHandler(Handler):
    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        ReturnResult(PortfolioVersionLoadStep.key),
    ]
