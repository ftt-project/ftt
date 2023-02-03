from result import Result, as_result, Ok, Err

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas, models
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository
from ftt.storage.repositories.weights_repository import WeightsRepository


class PortfolioVersionWeightedSecuritiesLoadStep(AbstractStep):
    key = "portfolio_version_weighted_securities"

    @classmethod
    def process(
        cls, portfolio_version: schemas.PortfolioVersion
    ) -> Result[list[schemas.WeightedSecurity], str]:
        if portfolio_version.id is None:
            return Ok([])

        portfolio_version_record = as_result(Exception)(
            PortfolioVersionsRepository.get_by_id
        )
        portfolio_version_result = portfolio_version_record(portfolio_version)

        match portfolio_version_result:
            case Err(models.PortfolioVersion.DoesNotExist()):
                return Err(
                    f"Portfolio Version with ID {portfolio_version.id} does not exist."
                )

        get_by_portfolio_version = as_result(Exception)(
            WeightsRepository.get_by_portfolio_version
        )
        weights_result = get_by_portfolio_version(portfolio_version=portfolio_version)

        match weights_result:
            case Err(Exception()):
                return Err(
                    f"Failed to load weights of Portfolio Version: {portfolio_version}. "
                    f"Reason: {weights_result.unwrap_err()}"
                )

        find_by_portfolio_version = as_result(Exception)(
            PortfoliosRepository.find_by_portfolio_version
        )
        portfolio_result = find_by_portfolio_version(
            portfolio_version=portfolio_version
        )

        match portfolio_result:
            case Err(models.Portfolio.DoesNotExist()):
                return Err(
                    f"Portfolio of Portfolio Version with ID {portfolio_version.id} does not exist."
                )

        weighted_securities = [
            schemas.WeightedSecurity(
                symbol=weight.security.symbol,
                portfolio=portfolio_result.unwrap(),
                portfolio_version=portfolio_version,
                security=weight.security,
                position=weight.position,
                planned_position=weight.planned_position,
                amount=weight.amount,
            )
            for weight in weights_result.unwrap()
        ]
        return Ok(weighted_securities)
