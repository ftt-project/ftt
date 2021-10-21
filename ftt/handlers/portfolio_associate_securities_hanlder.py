from ftt.handlers.handler.context import Context
from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.retrun_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_prepare_empty_weights_step import (
    PortfolioPrepareEmptyWeightsStep,
)
from ftt.handlers.portfolio_steps.portfolio_weights_persist_step import (
    PortfolioWeightsPersistStep,
)


class PortfolioAssociateSecuritiesHandler(Handler):
    handlers = [
        (PortfolioPrepareEmptyWeightsStep, "securities"),
        Context(assign=True, to="persist"),
        (
            PortfolioWeightsPersistStep,
            PortfolioPrepareEmptyWeightsStep.key,
            "portfolio_version",
            "persist",
        ),
        ReturnResult("portfolio_version"),
    ]
