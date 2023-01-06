from typing import List, Optional

from result import Ok, Result, as_result, Err

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas, models
from ftt.storage.repositories.weights_repository import WeightsRepository


class WeightsLoadStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(
        cls, portfolio_version: schemas.PortfolioVersion
    ) -> Result[List[schemas.Weight], Optional[str]]:
        get_by_portfolio_version = as_result(Exception)(
            WeightsRepository.get_by_portfolio_version
        )
        result = get_by_portfolio_version(portfolio_version)

        match result:
            case Ok(_):
                return result
            case Err(models.PortfolioVersion.DoesNotExist()):
                return Err(
                    f"Portfolio Version with ID {portfolio_version.id} does not exist"
                )
