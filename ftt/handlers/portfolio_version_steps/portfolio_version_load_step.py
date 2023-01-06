from result import Err, Result, as_result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas, models
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionLoadStep(AbstractStep):
    """
    Loads portfolio_management version from database by its ID
    """

    key = "portfolio_version"

    @classmethod
    def process(
        cls, portfolio_version: schemas.PortfolioVersion
    ) -> Result[schemas.PortfolioVersion, str]:
        get_by_id = as_result(Exception)(PortfolioVersionsRepository.get_by_id)
        result = get_by_id(portfolio_version)

        match result:
            case Err(models.PortfolioVersion.DoesNotExist()):
                return Err(
                    f"Portfolio Version with ID {portfolio_version.id} does not exist"
                )

        return result
