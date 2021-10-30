from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_deactivate_all_versions_step import (
    PortfolioDeactivateAllVersionsStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_activate_step import (
    PortfolioVersionActivateStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_activation_validate_step import (
    PortfolioVersionActivationValidateStep,
)


class PortfolioVersionActivationHandler(Handler):
    handlers = [
        (PortfolioVersionActivationValidateStep, "portfolio_version"),
        (PortfolioDeactivateAllVersionsStep, "portfolio"),
        (PortfolioVersionActivateStep, "portfolio_version"),
        (ReturnResult, PortfolioVersionActivateStep.key),
    ]
