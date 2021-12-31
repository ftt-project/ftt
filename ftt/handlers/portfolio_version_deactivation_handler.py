from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_deactivate_step import (
    PortfolioVersionDeactivateStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_deactivation_validate_step import (
    PortfolioVersionDeactivationValidateStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)


class PortfolioVersionDeactivationHandler(Handler):
    params = ("portfolio_version_id",)

    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        (PortfolioVersionDeactivationValidateStep, PortfolioVersionLoadStep.key),
        (PortfolioVersionDeactivateStep, PortfolioVersionLoadStep.key),
        (ReturnResult, PortfolioVersionDeactivateStep.key),
    ]
