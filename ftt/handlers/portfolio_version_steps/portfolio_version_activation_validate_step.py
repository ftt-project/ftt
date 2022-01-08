from typing import Optional

from result import Ok, Err, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionActivationValidateStep(AbstractStep):
    """
    Performs validation of portfolio version before activation

    * Checks if portfolio version is not already activated
    * Checks if portfolio version has associated weights
    """

    key = "portfolio_version_activation_validation"

    @classmethod
    def process(
        cls, portfolio_version: PortfolioVersion
    ) -> Result[PortfolioVersion, Optional[str]]:
        version = PortfolioVersionsRepository.get_active_version(
            portfolio_version.portfolio
        )

        if version == portfolio_version:
            return Err(f"Portfolio version #{portfolio_version.id} is already active")

        if portfolio_version.weights.count() == 0:
            return Err(
                f"Portfolio version #{portfolio_version.id} does not have any "
                "weights associated. Run balance step first."
            )

        for weight in portfolio_version.weights:
            if weight.planned_position == 0:
                return Err(
                    f"Portfolio version #{portfolio_version.id} has {weight.security.symbol} with "
                    "zero planned weight. Run balance step first."
                )

        return Ok(portfolio_version)
