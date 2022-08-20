from ftt.handlers.backtrading_steps.backtrading_run_step import BacktradingRunStep
from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_load_securties_step import (
    PortfolioVersionLoadSecuritiesStep,
)
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)
from ftt.handlers.security_prices_steps.security_prices_dataframe_load_step import (
    SecurityPricesDataframeLoadStep,
)


class BacktradeHandler(Handler):
    params = ("portfolio_version_id",)

    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        (PortfolioVersionLoadSecuritiesStep, PortfolioVersionLoadStep.key),
        (
            SecurityPricesDataframeLoadStep,
            PortfolioVersionLoadStep.key,
            PortfolioVersionLoadSecuritiesStep.key,
        ),
        (
            BacktradingRunStep,
            PortfolioVersionLoadStep.key,
            SecurityPricesDataframeLoadStep.key,
        ),
        (ReturnResult, BacktradingRunStep.key),
    ]
