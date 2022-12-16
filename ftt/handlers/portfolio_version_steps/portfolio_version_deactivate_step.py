from typing import Optional

from result import Ok, Result, as_result, Err

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas, models
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionDeactivateStep(AbstractStep):
    """
    Deactivate a portfolio version.
    """

    key = "deactivated_portfolio_version"

    @classmethod
    def process(
        cls, portfolio_version: Optional[schemas.PortfolioVersion]
    ) -> Result[schemas.PortfolioVersion, str]:
        if not portfolio_version:
            return Ok()

        portfolio_version.active = False

        update = as_result(Exception)(PortfolioVersionsRepository.update)
        result = update(portfolio_version)

        match result:
            case Ok(updated_portfolio_version):
                return Ok(updated_portfolio_version)
            case Err(models.PortfolioVersion.DoesNotExist()):
                return Err(
                    f"Portfolio Version with ID {portfolio_version.id} does not exist"
                )
