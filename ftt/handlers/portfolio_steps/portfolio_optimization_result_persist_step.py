from typing import Optional

from result import Ok, Result, as_result, Err

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)
from ftt.storage.repositories.securities_repository import SecuritiesRepository
from ftt.storage.repositories.weights_repository import WeightsRepository


class PortfolioOptimizationResultPersistStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(
        cls,
        portfolio_version: schemas.PortfolioVersion,
        portfolio_version_allocation: schemas.PortfolioAllocation,
    ) -> Result[list[schemas.Weight], Optional[str]]:
        result = []

        for symbol, qty in portfolio_version_allocation.allocation.items():
            security = SecuritiesRepository.get_by_name(symbol)
            weight = WeightsRepository.upsert(
                {
                    "portfolio_version": portfolio_version,
                    "security": security,
                    "position": 0,
                    "planned_position": qty,
                }
            )
            result.append(weight)

        portfolio_version.expected_annual_return = (
            portfolio_version_allocation.expected_annual_return
        )
        portfolio_version.annual_volatility = (
            portfolio_version_allocation.annual_volatility
        )
        portfolio_version.sharpe_ratio = portfolio_version_allocation.sharpe_ratio

        update = as_result(Exception)(PortfolioVersionsRepository.update)
        match update(portfolio_version):
            case Err(e):
                return Err(f"Error while updating portfolio version: {e}")

        # TODO: use schema entity instead of Weight model
        return Ok(result)
