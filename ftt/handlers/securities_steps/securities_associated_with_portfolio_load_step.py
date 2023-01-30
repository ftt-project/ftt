from typing import Optional

from result import Result, Err, as_result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas, models
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class SecuritiesAssociatedWithPortfolioLoadStep(AbstractStep):
    key = "securities"

    @classmethod
    def process(
        cls, portfolio: schemas.Portfolio
    ) -> Result[list[schemas.Security], Optional[str]]:
        find_by_portfolio = as_result(Exception)(SecuritiesRepository.find_by_portfolio)
        securities_result = find_by_portfolio(portfolio)

        match securities_result:
            case Err(models.Portfolio.DoesNotExist()):
                return Err(f"Portfolio with id {portfolio.id} not found")
            case Err(_):
                return Err(securities_result.unwrap_err())

        if len(securities_result.unwrap()) == 0:
            return Err(f"No securities associated with portfolio {portfolio.id}")

        return securities_result
