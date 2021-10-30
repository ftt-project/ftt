from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_deactivate_step import (
    PortfolioVersionDeactivateStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_deactivation_validate_step import (
    PortfolioVersionDeactivationValidateStep,
)


class PortfolioVersionDeactivationHandler(Handler):
    params = ("portfolio", "portfolio_version")

    handlers = [
        (PortfolioVersionDeactivationValidateStep, "portfolio_version"),
        (PortfolioVersionDeactivateStep, "portfolio_version"),
        (ReturnResult, PortfolioVersionDeactivateStep.key),
    ]
