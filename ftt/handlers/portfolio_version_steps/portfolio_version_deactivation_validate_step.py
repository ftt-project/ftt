from result import Ok, Err, Result, as_result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionDeactivationValidateStep(AbstractStep):
    """
    Validate if the portfolio_management version can be deactivated.

    * checks if the portfolio_management version is active
    """

    key = "portfolio_version_deactivation_validation"

    @classmethod
    def process(
        cls, portfolio_version: schemas.PortfolioVersion
    ) -> Result[schemas.PortfolioVersion, str]:
        get_by_id = as_result(Exception)(PortfolioVersionsRepository.get_by_id)
        result = get_by_id(portfolio_version)

        match result:
            case Err(PortfolioVersion.DoesNotExist()):
                return Err(
                    f"Portfolio Version with ID {portfolio_version.id} does not exist"
                )
            case Ok(record):
                if not record.active:
                    return Err(f"Portfolio version #{record.id} is not active")

        return Ok(portfolio_version)
