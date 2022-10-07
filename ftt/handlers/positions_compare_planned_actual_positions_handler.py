from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)
from ftt.handlers.position_steps.compare_planned_actual_positions_step import (
    ComparePlannedActualPositionsStep,
)
from ftt.handlers.weights_steps.weights_load_step import WeightsLoadStep


class PositionsComparePlannedActualPositionsHandler(Handler):
    params = ("portfolio_version_id", "open_positions")

    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        (WeightsLoadStep, PortfolioVersionLoadStep.key),
        (ComparePlannedActualPositionsStep, WeightsLoadStep.key, "open_positions"),
        (ReturnResult, ComparePlannedActualPositionsStep.key),
    ]
