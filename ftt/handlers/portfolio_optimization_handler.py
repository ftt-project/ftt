from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_weights_persist_step import (
    PortfolioWeightsPersistStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_allocation_step import (
    PortfolioVersionAllocationStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_optimization_step import (
    PortfolioVersionOptimizationStep,
)
from ftt.handlers.security_prices_steps.security_prices_load_step import (
    SecurityPricesLoadStep,
)


class PortfolioOptimizationHandler(Handler):
    params = (
        "portfolio_version_id",
        "optimization_strategy_name",
        "allocation_strategy_name",
    )

    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        (SecurityPricesLoadStep, PortfolioVersionLoadStep.key),
        (
            PortfolioVersionOptimizationStep,
            PortfolioVersionLoadStep.key,
            SecurityPricesLoadStep.key,
            "optimization_strategy_name",
        ),
        (
            PortfolioVersionAllocationStep,
            PortfolioVersionLoadStep.key,
            SecurityPricesLoadStep.key,
            PortfolioVersionOptimizationStep.key,
            "allocation_strategy_name",
        ),
        (
            PortfolioWeightsPersistStep,
            PortfolioVersionLoadStep.key,
            PortfolioVersionAllocationStep.key,
        ),
        (ReturnResult, PortfolioWeightsPersistStep.key),
    ]
