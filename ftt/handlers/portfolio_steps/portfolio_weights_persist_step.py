from typing import List, Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.portfolio_management.dtos import PortfolioAllocationDTO
from ftt.storage.models import Weight
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.repositories.securities_repository import SecuritiesRepository
from ftt.storage.repositories.weights_repository import WeightsRepository


class PortfolioWeightsPersistStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(
        cls,
        portfolio_version: PortfolioVersion,
        portfolio_version_allocation: PortfolioAllocationDTO,
    ) -> Result[List[Weight], Optional[str]]:
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
        portfolio_version.save()

        return Ok(result)
