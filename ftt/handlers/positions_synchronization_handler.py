from ftt.brokers.brokerage_service import BrokerageService
from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.order_steps.orders_create_step import OrdersCreateStep
from ftt.handlers.order_steps.orders_place_step import OrdersPlaceStep
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
from ftt.storage import schemas


class PositionsSynchronizationHandler(Handler):
    params = {
        "portfolio_version": schemas.PortfolioVersion,
        "brokerage_service": BrokerageService,
    }

    handlers = [
        (RequestOpenPositionsStep, "brokerage_service"),
        (PortfolioVersionLoadStep, "portfolio_version"),
        (PortfolioVersionLoadPortfolioStep, PortfolioVersionLoadStep.key),
        (WeightsLoadStep, PortfolioVersionLoadStep.key),
        (
            ComparePlannedActualPositionsStep,
            WeightsLoadStep.key,
            RequestOpenPositionsStep.key,
        ),
        (
            OrdersCreateStep,
            ComparePlannedActualPositionsStep.key,
            WeightsLoadStep.key,
            PortfolioVersionLoadStep.key,
            PortfolioVersionLoadPortfolioStep.key,
        ),
        (OrdersPlaceStep, OrdersCreateStep.key, "brokerage_service"),
        (ReturnResult, OrdersPlaceStep.key),
    ]
