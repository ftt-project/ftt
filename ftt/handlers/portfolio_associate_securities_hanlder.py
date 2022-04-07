from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_associate_empty_weights_step import (
    PortfolioVersionAssociateEmptyWeightsStep,
)


class PortfolioAssociateSecuritiesHandler(Handler):
    params = ("securities", "portfolio_version")

    handlers = [
        (
            PortfolioVersionAssociateEmptyWeightsStep,
            "portfolio_version",
            "securities",
        ),
        (ReturnResult, "portfolio_version"),
    ]
