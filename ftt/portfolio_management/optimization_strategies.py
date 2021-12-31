import riskfolio as rp
from riskfolio import Sharpe

from ftt.portfolio_management import PortfolioAllocationDTO


class HistoricalOptimizationStrategy:
    def __init__(self, returns):
        self.returns = returns
        self.portfolio = rp.Portfolio(returns=returns)

    def optimize(self):
        self.portfolio.assets_stats()
        model = "Classic"  # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
        rm = "MV"  # Risk measure used, this time will be variance
        obj = (
            "Sharpe"  # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
        )
        hist = (
            True  # Use historical scenarios for risk measures that depend on scenarios
        )
        rf = 0  # Risk free rate
        risk_aversion = 0  # Risk aversion factor, only useful when obj is 'Utility'
        weights = self.portfolio.optimization(
            model=model, rm=rm, obj=obj, rf=rf, l=risk_aversion, hist=hist
        )
        sharpe = Sharpe(
            weights,
            mu=self.portfolio.mu,
            returns=self.returns,
            cov=self.portfolio.cov,
            rf=rf,
        )

        return PortfolioAllocationDTO(
            weights=weights.to_dict()["weights"],
            sharpe_ratio=sharpe,
            cov_matrix=self.portfolio.cov,
        )
