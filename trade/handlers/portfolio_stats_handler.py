from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_steps.portfolio_weights_allocation_step import (
    PortfolioWeightsAllocationStep,
)


class PortfoliosStatsHandler(Handler):
    params = ["portfolio_version"]

    handlers = [
        (PortfolioWeightsAllocationStep, "portfolio_version"),
        ReturnResult("stats"),
    ]
