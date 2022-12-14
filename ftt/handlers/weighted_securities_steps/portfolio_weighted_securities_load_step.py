from result import Ok, as_result, Result, Err

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas, models
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class PortfolioWeightedSecuritiesLoadStep(AbstractStep):
    key = "portfolio_weighted_securities"

    @classmethod
    def process(
        cls, portfolio: schemas.Portfolio
    ) -> Result[list[schemas.WeightedSecurity], str]:
        find_by_portfolio = as_result(Exception)(SecuritiesRepository.find_by_portfolio)
        securities_result: Result[list[schemas.Security]] = find_by_portfolio(
            portfolio=portfolio
        )

        match securities_result:
            case Err(models.Portfolio.DoesNotExist()):
                return Err(f"Portfolio with ID {portfolio.id} does not exist.")

        weighted_securities = [
            schemas.WeightedSecurity(
                symbol=security.symbol,
                portfolio=portfolio,
                security=security,
            )
            for security in securities_result.unwrap()
        ]
        return Ok(weighted_securities)
