from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult
from ftt.handlers.portfolio_version_steps.portfolio_version_load_step import (
    PortfolioVersionLoadStep,
)
from ftt.handlers.weights_steps.weights_delete_step import WeightsDeleteStep


class PortfolioVersionSecuritiesDisassociateHandler(Handler):
    params = ("portfolio_version_id", "securities")

    handlers = [
        (PortfolioVersionLoadStep, "portfolio_version_id"),
        (WeightsDeleteStep, PortfolioVersionLoadStep.key, "securities"),
        (ReturnResult, PortfolioVersionLoadStep.key, WeightsDeleteStep.key),
    ]
