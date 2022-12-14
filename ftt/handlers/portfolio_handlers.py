from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.weighted_securities_steps.combine_weighted_securities_step import (
    CombineWeightedSecuritiesStep,
)
from ftt.handlers.weighted_securities_steps.portfolio_version_weighted_securities_load_step import (
    PortfolioVersionWeightedSecuritiesLoadStep,
)
from ftt.handlers.weighted_securities_steps.portfolio_weighted_securities_load_step import (
    PortfolioWeightedSecuritiesLoadStep,
)
from ftt.storage import schemas


class PortfolioSecuritiesAndWeightsLoadHandler(Handler):
    """
    Loads PortfolioSecurity objects by given Portfolio
    and returns schemas.Weight as a generic representation of the
    weight on a level of Portfolio.

    It combines PortfolioSecurities with Weights and gives a unified
    picture of securities on Portfolio weighted or not.
    """

    params = {
        "portfolio": schemas.Portfolio,
        "portfolio_version": schemas.PortfolioVersion,
    }

    handlers = [
        (PortfolioWeightedSecuritiesLoadStep, "portfolio"),
        (PortfolioVersionWeightedSecuritiesLoadStep, "portfolio_version"),
        (
            CombineWeightedSecuritiesStep,
            PortfolioWeightedSecuritiesLoadStep.key,
            PortfolioVersionWeightedSecuritiesLoadStep.key,
        ),
        (ReturnResult, CombineWeightedSecuritiesStep.key),
    ]
