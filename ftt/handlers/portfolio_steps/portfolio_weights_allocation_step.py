from typing import Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models.portfolio_version import PortfolioVersion


class PortfolioWeightsAllocationStep(AbstractStep):
    key = "stats"

    @classmethod
    def process(
        cls, portfolio_version: PortfolioVersion
    ) -> Result[dict, Optional[str]]:
        allocations = {
            weight.security.symbol: weight.planned_position
            for weight in portfolio_version.weights
        }
        return Ok({"planned_weights": allocations})
