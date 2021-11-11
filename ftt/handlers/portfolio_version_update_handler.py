from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_update_step import (
    PortfolioVersionUpdateStep,
)


class PortfolioVersionUpdateHandler(Handler):
    params = (
        "portfolio_version",
        "params",
    )

    handlers = [
        (PortfolioVersionUpdateStep, "portfolio_version", "params"),
        (ReturnResult, PortfolioVersionUpdateStep.key),
    ]
