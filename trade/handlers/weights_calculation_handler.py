from trade.handlers.handler.handler import Handler


class WeightsCalculationHandler(Handler):
    handlers = [
        # (PortfolioSecuritiesLoadStep, "portfolio"),
        # (PortfolioSecurityPricesLoadStep, "portfolio"),
        # (PortfolioWeightsCalculateStep, "portfolio"),
        # (PortfolioWeightsPersistStep, PortfolioWeightsCalculateStep.key, "portfolio"),
        # (SecuritiesInfoDownloadStep, PortfolioWeightsPersistStep.key)
    ]