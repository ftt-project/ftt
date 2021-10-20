from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_steps.portfolio_deactivate_all_versions_step import (
    PortfolioDeactivateAllVersionsStep,
)
from trade.handlers.portfolio_version_steps.portfolio_version_activate_step import (
    PortfolioVersionActivateStep,
)
from trade.handlers.portfolio_version_steps.portfolio_version_activation_validate_step import (
    PortfolioVersionActivationValidateStep,
)


class PortfolioVersionActivationHandler(Handler):
    handlers = [
        (PortfolioVersionActivationValidateStep, "portfolio_version"),
        (PortfolioDeactivateAllVersionsStep, "portfolio"),
        (PortfolioVersionActivateStep, "portfolio_version"),
        ReturnResult(PortfolioVersionActivateStep.key),
    ]
