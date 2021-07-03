from typing import Tuple
from result import Ok
from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models import PortfolioVersion
from trade.storage.repositories import SecuritiesRepository, WeightsRepository


class PortfolioWeightsPersistStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(
        cls,
        portfolio_version: PortfolioVersion,
        weights: Tuple[dict, float],
        persist: bool,
    ) -> Ok:
        result = []
        if not persist:
            return Ok(result)

        quantities, _ = weights
        for symbol, qty in quantities.items():
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

        return Ok(result)
