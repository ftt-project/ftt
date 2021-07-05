from result import Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models.portfolio_version import PortfolioVersion


class PortfolioWeightsAllocationStep(AbstractStep):
    key = "stats"

    @classmethod
    def process(cls, portfolio_version: PortfolioVersion) -> OkErr:
        allocations = {weight.security.symbol: weight.planned_position for weight in portfolio_version.weights}
        return Ok({
            "planned_weights": allocations
        })
