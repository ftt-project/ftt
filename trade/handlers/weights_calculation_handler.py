from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_steps.portfolio_securities_load_step import (
    PortfolioSecuritiesLoadStep,
)
from trade.handlers.portfolio_steps.portfolio_weights_persist_step import (
    PortfolioWeightsPersistStep,
)
from trade.handlers.security_prices_steps.security_prices_dataframe_load_step import (
    SecurityPricesDataframeLoadStep,
)
from trade.handlers.weights_steps.weights_calculate_step import WeightsCalculateStep


class WeightsCalculationHandler(Handler):
    handlers = [
        (PortfolioSecuritiesLoadStep, "portfolio"),
        (
            SecurityPricesDataframeLoadStep,
            PortfolioSecuritiesLoadStep.key,
            "start_period",
            "end_period",
            "interval",
        ),
        (WeightsCalculateStep, SecurityPricesDataframeLoadStep.key, "portfolio"),
        (
            PortfolioWeightsPersistStep,
            WeightsCalculateStep.key,
            "portfolio_version",
            "persist",
        ),
        ReturnResult(PortfolioWeightsPersistStep.key),
    ]
