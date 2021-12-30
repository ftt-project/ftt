from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_weights_allocation_step import (
    PortfolioWeightsAllocationStep,
)


class PortfoliosStatsHandler(Handler):
    params = ("portfolio_version",)

    handlers = [
        (PortfolioWeightsAllocationStep, "portfolio_version"),
        (ReturnResult, PortfolioWeightsAllocationStep.key),
    ]
