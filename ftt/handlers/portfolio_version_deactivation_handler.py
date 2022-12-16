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
from ftt.storage import schemas


class PortfolioVersionDeactivationHandler(Handler):
    params = {"portfolio_version": schemas.PortfolioVersion}

    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version"),
        (PortfolioVersionDeactivationValidateStep, PortfolioVersionLoadStep.key),
        (PortfolioVersionDeactivateStep, PortfolioVersionLoadStep.key),
        (ReturnResult, PortfolioVersionDeactivateStep.key),
    ]
