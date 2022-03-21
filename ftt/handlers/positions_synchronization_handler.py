from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.order_steps.create_orders_step import CreateOrdersStep
from ftt.handlers.order_steps.place_orders_step import PlaceOrdersStep
from ftt.handlers.portfolio_version_steps.portfolio_version_load_portfolio_step import (
    PortfolioVersionLoadPortfolioStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)
from ftt.handlers.position_steps.compare_planned_actual_positions_step import (
    ComparePlannedActualPositionsStep,
)
from ftt.handlers.position_steps.request_open_positions_step import (
    RequestOpenPositionsStep,
)
from ftt.handlers.weights_steps.weights_load_step import WeightsLoadStep


class PositionsSynchronizationHandler(Handler):
    params = ("portfolio_version_id",)

    handlers = [
        (RequestOpenPositionsStep,),
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        (PortfolioVersionLoadPortfolioStep, PortfolioVersionLoadStep.key),
        (WeightsLoadStep, PortfolioVersionLoadStep.key),
        (
            ComparePlannedActualPositionsStep,
            WeightsLoadStep.key,
            RequestOpenPositionsStep.key,
        ),
        (
            CreateOrdersStep,
            ComparePlannedActualPositionsStep.key,
            WeightsLoadStep.key,
            PortfolioVersionLoadStep.key,
            PortfolioVersionLoadPortfolioStep.key,
        ),
        (PlaceOrdersStep, CreateOrdersStep.key),
        (ReturnResult, PlaceOrdersStep.key),
    ]
