from result import OkErr, Ok, Err

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion


class PortfolioVersionDeactivationValidateStep(AbstractStep):
    """
    Validate if the portfolio version can be deactivated.

    * checks if the portfolio version is active
    """

    key = "portfolio_version_deactivation_validation"

    @classmethod
    def process(cls, portfolio_version: PortfolioVersion) -> OkErr:
        if portfolio_version.active:
            return Ok(portfolio_version)
        else:
            return Err(f"Portfolio version #{portfolio_version.id} is not active")
