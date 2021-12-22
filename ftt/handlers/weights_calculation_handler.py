from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_securities_load_step import (
    PortfolioSecuritiesLoadStep,
)
from ftt.handlers.portfolio_steps.portfolio_weights_persist_step import (
    PortfolioWeightsPersistStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)
from ftt.handlers.security_prices_steps.security_prices_dataframe_load_step import (
    SecurityPricesDataframeLoadStep,
)
from ftt.handlers.weights_steps.weights_calculate_step import WeightsCalculateStep


class WeightsCalculationHandler(Handler):
    """
    Handler for calculating weights for a portfolio version.
    """

    params = (
        "portfolio_version",
        "start_period",
        "end_period",
        "interval",
        "persist",
    )

    handlers = [
        (PortfolioSecuritiesLoadStep, PortfolioVersionLoadStep.key),
        (
            SecurityPricesDataframeLoadStep,
            PortfolioSecuritiesLoadStep.key,
            "start_period",
            "end_period",
            "interval",
        ),
        (
            WeightsCalculateStep,
            SecurityPricesDataframeLoadStep.key,
            "portfolio_version",
        ),
        (
            PortfolioWeightsPersistStep,
            WeightsCalculateStep.key,
            "portfolio_version",
            "persist",
        ),
        (ReturnResult, PortfolioWeightsPersistStep.key),
    ]
