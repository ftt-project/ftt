from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_version_steps.portfolio_version_deactivate_step import (
    PortfolioVersionDeactivateStep,
)
from trade.handlers.portfolio_version_steps.portfolio_version_deactivation_validate_step import (
    PortfolioVersionDeactivationValidateStep,
)


class PortfolioVersionDeactivationHandler(Handler):
    handlers = [
        (PortfolioVersionDeactivationValidateStep, "portfolio_version"),
        (PortfolioVersionDeactivateStep, "portfolio_version"),
        ReturnResult(PortfolioVersionDeactivateStep.key),
    ]
