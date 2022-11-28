from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_associate_empty_weights_step import (
    PortfolioVersionAssociateEmptyWeightsStep,
)


class PortfolioVersionAssociateSecuritiesHandler(Handler):
    """
    Associate securities with portfolio version.

    At the moment of writing this handler the way to associate securities with portfolio is to
    associate portfolio through weights with portfolio version model.

    The new approach is to associate securities with portfolio version through portfolio securities HBTM model.
    """

    params = ("securities", "portfolio_version")

    handlers = [
        (
            PortfolioVersionAssociateEmptyWeightsStep,
            "portfolio_version",
            "securities",
        ),
        (ReturnResult, "portfolio_version"),
    ]
