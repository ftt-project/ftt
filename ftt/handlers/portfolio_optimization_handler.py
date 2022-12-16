from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_optimization_result_persist_step import (
    PortfolioOptimizationResultPersistStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_allocation_step import (
    PortfolioVersionAllocationStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_load_portfolio_step import (
    PortfolioVersionLoadPortfolioStep,
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
from ftt.storage import schemas


class PortfolioOptimizationHandler(Handler):
    params = {
        "portfolio_version": schemas.PortfolioVersion,
    }

    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version"),
        (PortfolioVersionLoadPortfolioStep, PortfolioVersionLoadStep.key),
        (
            SecurityPricesLoadStep,
            PortfolioVersionLoadStep.key,
            PortfolioVersionLoadPortfolioStep.key,
        ),
        (
            PortfolioVersionOptimizationStep,
            PortfolioVersionLoadStep.key,
            SecurityPricesLoadStep.key,
        ),
        (
            PortfolioVersionAllocationStep,
            PortfolioVersionLoadStep.key,
            PortfolioVersionLoadPortfolioStep.key,
            SecurityPricesLoadStep.key,
            PortfolioVersionOptimizationStep.key,
        ),
        (
            PortfolioOptimizationResultPersistStep,
            PortfolioVersionLoadStep.key,
            PortfolioVersionAllocationStep.key,
        ),
        (ReturnResult, PortfolioOptimizationResultPersistStep.key),
    ]
