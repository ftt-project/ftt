from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import PortfolioVersionLoadStep
from ftt.handlers.position_steps.compare_planned_actual_positions_step import ComparePlannedActualPositionsStep
from ftt.handlers.position_steps.request_open_positions_step import RequestOpenPositionsStep
from ftt.handlers.weights_steps.weights_load_step import WeightsLoadStep


class PositionsComparePlannedActualPositionsHandler(Handler):
    params = ("portfolio_version_id", "brokerage_service")

    handlers = [
        (RequestOpenPositionsStep, "brokerage_service"),
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        (WeightsLoadStep, PortfolioVersionLoadStep.key),
        (
            ComparePlannedActualPositionsStep,
            WeightsLoadStep.key,
            RequestOpenPositionsStep.key,
        ),
        (ReturnResult, ComparePlannedActualPositionsStep.key),
    ]