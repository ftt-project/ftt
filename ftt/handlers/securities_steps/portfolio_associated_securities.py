from result import Result, as_result, Ok, Err

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas, models
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class PortfolioAssociatedSecuritiesStep(AbstractStep):
    """
    Loads Securities associated with Portfolio through PortfolioSecurity model.

    Parameters:
    ----------
        portfolio (schemas.Portfolio): Portfolio object

    Returns:
    --------
        Result[list[schemas.Security], str]: Result with list of Security
    """

    key = "portfolio_associated_securities"

    @classmethod
    def process(
        cls, portfolio: schemas.Portfolio
    ) -> Result[list[schemas.Security], str]:
        find_by_portfolio = as_result(Exception)(SecuritiesRepository.find_by_portfolio)
        securities_result = find_by_portfolio(portfolio)

        match securities_result:
            case Err(models.Portfolio.DoesNotExist()):
                return Err(f"Portfolio with ID {portfolio.id} is missing")

        return Ok(
            [
                schemas.Security.from_orm(security)
                for security in securities_result.unwrap()
            ]
        )
