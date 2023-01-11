from ftt.handlers.handler.context import Context
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
from ftt.handlers.securities_steps.securities_associated_with_portfolio_load_step import (
    SecuritiesAssociatedWithPortfolioLoadStep,
)
from ftt.handlers.security_prices_steps.securities_prices_download_step import (
    SecurityPricesDownloadStep,
)
from ftt.handlers.security_prices_steps.security_prices_load_step import (
    SecurityPricesLoadStep,
)
from ftt.handlers.security_prices_steps.security_prices_upsert_step import (
    SecurityPricesUpsertStep,
)
from ftt.storage import schemas


class PortfolioVersionOptimizationHandler(Handler):
    """
    Optimizes a portfolio version by given portfolio version id.

    Returns:
    --------
        Result[List[Weight], Optional[str]] - Result with list of weights and error message if any.
    """

    params = {
        "portfolio_version": schemas.PortfolioVersion,
    }

    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version"),
        (PortfolioVersionLoadPortfolioStep, PortfolioVersionLoadStep.key),
        (
            SecuritiesAssociatedWithPortfolioLoadStep,
            PortfolioVersionLoadPortfolioStep.key,
        ),
        Context(assign="on_missing", to="mode"),
        (
            SecurityPricesDownloadStep,
            SecuritiesAssociatedWithPortfolioLoadStep.key,
            PortfolioVersionLoadPortfolioStep.key,
            "mode",
        ),
        (
            SecurityPricesUpsertStep,
            SecurityPricesDownloadStep.key,
            PortfolioVersionLoadPortfolioStep.key,
        ),
        (
            SecurityPricesLoadStep,
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
