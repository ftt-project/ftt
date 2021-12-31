from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_steps.portfolio_prepare_empty_weights_step import (
    PortfolioPrepareEmptyWeightsStep,
)
from ftt.handlers.portfolio_steps.portfolio_weights_persist_step import (
    PortfolioWeightsPersistStep,
)


class PortfolioAssociateSecuritiesHandler(Handler):
    params = ("securities", "portfolio_version")

    handlers = [
        (PortfolioPrepareEmptyWeightsStep, "securities"),
        (
            PortfolioWeightsPersistStep,
            PortfolioPrepareEmptyWeightsStep.key,
            "portfolio_version",
        ),
        (ReturnResult, "portfolio_version"),
    ]
