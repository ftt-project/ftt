from trade.handlers.handler.handler import Handler
from trade.handlers.portfolio_steps.portfolio_securities_load_step import PortfolioSecuritiesLoadStep
from trade.handlers.security_prices_steps.security_prices_dataframe_load_step import SecurityPricesDataframeLoadStep


class WeightsCalculationHandler(Handler):
    handlers = [
        (PortfolioSecuritiesLoadStep, "portfolio"),
        (SecurityPricesDataframeLoadStep, PortfolioSecuritiesLoadStep.key),
        # (PortfolioWeightsCalculateStep, "portfolio"),
        # (PortfolioWeightsPersistStep, PortfolioWeightsCalculateStep.key, "portfolio"),
        # (SecuritiesInfoDownloadStep, PortfolioWeightsPersistStep.key)
    ]