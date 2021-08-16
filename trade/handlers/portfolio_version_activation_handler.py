from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_version_steps.portfolio_version_activate_step import (
    PortfolioVersionActivateStep,
)
from trade.handlers.portfolio_version_steps.portfolio_version_activation_validate_step import (
    PortfolioVersionActivationValidateStep,
)
from trade.handlers.portfolio_version_steps.portfolio_version_deactivate_step import (
    PortfolioVersionDeactivateStep,
)
from trade.handlers.portfolio_version_steps.portfolio_version_load_active_step import (
    PortfolioVersionLoadActiveStep,
)


class PortfolioVersionActivationHandler(Handler):
    handlers = [
        (PortfolioVersionActivationValidateStep, "portfolio_version"),
        (PortfolioVersionLoadActiveStep, "portfolio"),
        (PortfolioVersionDeactivateStep, PortfolioVersionLoadActiveStep.key),
        (PortfolioVersionActivateStep, "portfolio_version"),
        ReturnResult(PortfolioVersionActivateStep.key),
    ]
