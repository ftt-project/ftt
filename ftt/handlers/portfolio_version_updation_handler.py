from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_update_step import (
    PortfolioVersionUpdateStep,
)


class PortfolioVersionUpdationHandler(Handler):
    params = (
        "portfolio_version",
        "dto",
    )

    handlers = [
        (PortfolioVersionUpdateStep, "portfolio_version", "dto"),
        (ReturnResult, PortfolioVersionUpdateStep.key),
    ]
