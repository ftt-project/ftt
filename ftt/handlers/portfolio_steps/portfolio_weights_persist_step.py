from result import Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.handlers.weights_steps.weights_calculate_step import (
    WeightsCalculateStepResult,
)
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.repositories.securities_repository import SecuritiesRepository
from ftt.storage.repositories.weights_repository import WeightsRepository


class PortfolioWeightsPersistStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(
        cls,
        portfolio_version: PortfolioVersion,
        weights: WeightsCalculateStepResult,
        persist: bool,
    ) -> Ok:
        result = []
        if not persist:
            return Ok(result)

        for symbol, qty in weights.allocation.items():
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

        portfolio_version.expected_annual_return = weights.expected_annual_return
        portfolio_version.annual_volatility = weights.annual_volatility
        portfolio_version.sharpe_ratio = weights.sharpe_ratio
        portfolio_version.save()

        return Ok(result)
