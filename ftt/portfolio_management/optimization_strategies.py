import abc
from typing import ClassVar, Type

from ftt.portfolio_management.dtos import PortfolioAllocationDTO


class AbstractOptimizationStrategy(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "optimize") and callable(subclass.optimize)


class HistoricalOptimizationStrategy(AbstractOptimizationStrategy):
    def __init__(self, returns):
        from riskfolio import Portfolio  # type: ignore

        self.returns = returns
        self.portfolio = Portfolio(returns=returns)

    def optimize(self):
        from riskfolio import Sharpe

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
            allocation={},
        )


class RiskParityOptimizationStrategy(AbstractOptimizationStrategy):
    def __init__(self, returns):
        self.returns = returns
        from riskfolio import Portfolio

        self.portfolio = Portfolio(returns=returns)

    def optimize(self):
        # TODO: method_mu and method_cov must be options and accessible in CLI as options
        method_mu = (
            "hist"  # Method to estimate expected returns based on historical data.
        )
        method_cov = (
            "hist"  # Method to estimate covariance matrix based on historical data.
        )
        self.portfolio.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

        model = "Classic"  # Could be Classic (historical) or FM (Factor Model)
        rm = "MV"  # Risk measure used, this time will be variance
        hist = (
            True  # Use historical scenarios for risk measures that depend on scenarios
        )
        rf = 0  # Risk free rate
        b = None  # Risk contribution constraints vector

        weights = self.portfolio.rp_optimization(
            model=model, rm=rm, rf=rf, b=b, hist=hist
        )

        from riskfolio import Sharpe

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
            allocation={},
        )


class OptimizationStrategyResolver:
    _strategies: ClassVar[dict[str, Type[AbstractOptimizationStrategy]]] = {
        "historical": HistoricalOptimizationStrategy,
        "risk_parity": RiskParityOptimizationStrategy,
    }

    @classmethod
    def strategies(cls) -> list[str]:
        return list(cls._strategies.keys())

    @classmethod
    def resolve(cls, strategy_name: str) -> Type[AbstractOptimizationStrategy]:
        try:
            return cls._strategies[strategy_name]
        except KeyError:
            raise ValueError(f"Unknown optimization strategy {strategy_name}")
