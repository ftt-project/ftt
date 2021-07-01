from trade.handlers.handler.context import Context
from trade.handlers.handler.handler import Handler
from trade.handlers.handler.retrun_result import ReturnResult
from trade.handlers.portfolio_steps.portfolio_prepare_empty_weights_step import PortfolioPrepareEmptyWeightsStep
from trade.handlers.portfolio_steps.portfolio_weights_persist_step import PortfolioWeightsPersistStep


class PortfolioAssociateSecuritiesHandler(Handler):
    handlers = [
        (PortfolioPrepareEmptyWeightsStep, "securities"),
        Context(assign=True, to="persist"),
        (PortfolioWeightsPersistStep, PortfolioPrepareEmptyWeightsStep.key, "portfolio_version", "persist"),
        ReturnResult("portfolio_version")
    ]