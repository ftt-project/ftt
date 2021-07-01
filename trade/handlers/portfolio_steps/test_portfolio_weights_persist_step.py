from typing import Tuple
from result import Ok
from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models import PortfolioVersion
from trade.storage.repositories import SecuritiesRepository, WeightsRepository


class PortfolioWeightsPersistStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(cls, portfolio_version: PortfolioVersion, calculated_weights: Tuple[dict, float], persist: bool) -> Ok:
        weights = []
        if not persist:
            return Ok(weights)

        quantities, _ = calculated_weights
        for symbol, qty in quantities.items():
            security = SecuritiesRepository.get_by_name(symbol)
            weight = WeightsRepository.upsert({
                "portfolio_version": portfolio_version,
                "ticker": security,
                "position": 0,
                "planned_position": qty
            })
            weights.append(weight)

        return Ok(weights)
