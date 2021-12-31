from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_deactivate_all_versions_step import (
    PortfolioDeactivateAllVersionsStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_activate_step import (
    PortfolioVersionActivateStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_activation_validate_step import (
    PortfolioVersionActivationValidateStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_load_portfolio_step import (
    PortfolioVersionLoadPortfolioStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)


class PortfolioVersionActivationHandler(Handler):
    """
    This handler performs all necessary operations to activate a portfolio version.

    * Checks if the portfolio version is not active already
    * Checks if the portfolio version has associated weights
    * Deactivates all versions of the associated portfolio
    * Activates a portfolio version by ID
    """

    params = ("portfolio_version_id",)

    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        (PortfolioVersionActivationValidateStep, PortfolioVersionLoadStep.key),
        (PortfolioVersionLoadPortfolioStep, PortfolioVersionLoadStep.key),
        (PortfolioDeactivateAllVersionsStep, PortfolioVersionLoadPortfolioStep.key),
        (PortfolioVersionActivateStep, PortfolioVersionLoadStep.key),
        (ReturnResult, PortfolioVersionActivateStep.key),
    ]
