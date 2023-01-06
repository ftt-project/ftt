import numpy as np
import pandas as pd

from ftt.storage import schemas


class DefaultAllocationStrategy:
    def __init__(
        self,
        portfolio_allocation: schemas.PortfolioAllocation,
        value: float,
        latest_prices: dict[str, float],
    ):
        self.portfolio_allocation = portfolio_allocation
        self.value = value
        self.latest_prices = pd.Series(latest_prices)

    def allocate(self) -> schemas.PortfolioAllocation:
        from pypfopt import DiscreteAllocation  # type: ignore
        from pypfopt.base_optimizer import BaseOptimizer, portfolio_performance  # type: ignore

        optimizer = BaseOptimizer(len(self.latest_prices))
        weights = pd.Series(self.portfolio_allocation.weights)
        optimizer.set_weights(weights)
        cleaned_weights = optimizer.clean_weights()

        mu, sigma, sharpe = portfolio_performance(
            weights, self.latest_prices, self.portfolio_allocation.cov_matrix
        )

        da = DiscreteAllocation(
            cleaned_weights,
            self.latest_prices,
            total_portfolio_value=float(self.value),
        )
        alloc, leftover = da.lp_portfolio()

        self.__set_expected_annual_return(mu)
        self.__set_annual_volatility(sigma)
        self.portfolio_allocation.allocation = self.__normalize_allocation(
            weights.keys().to_list(), alloc
        )
        self.portfolio_allocation.leftover = leftover

        return self.portfolio_allocation

    def __normalize_allocation(self, symbols, allocation):
        """
        Allocation by default comes in as a dict of symbol index and amount.
        Weights that are too small are ignored.
        This function returns a dict of symbol and amount with zeros included.
        """
        w = dict(zip(symbols, np.zeros(len(symbols)).tolist()))
        for index, (symbol, sw) in enumerate(w.items()):
            if index in allocation:
                w[symbol] = allocation[index]

        return w

    def __set_expected_annual_return(self, mu):
        if (
            self.portfolio_allocation.expected_annual_return is not None
            and self.portfolio_allocation.expected_annual_return != mu
        ):
            raise ValueError(
                "Expected annual return is already set "
                f"{self.portfolio_allocation.expected_annual_return} does not match actual {mu}"
            )
        self.portfolio_allocation.expected_annual_return = mu

    def __set_annual_volatility(self, sigma):
        if (
            self.portfolio_allocation.annual_volatility is not None
            and self.portfolio_allocation.annual_volatility != sigma
        ):
            raise ValueError(
                "Expected volatility is already set "
                f"{self.portfolio_allocation.annual_volatility} does not match actual {sigma}"
            )
        self.portfolio_allocation.annual_volatility = sigma


class AllocationStrategyResolver:
    _strategies = ["default"]

    @classmethod
    def strategies(cls) -> list[str]:
        return cls._strategies

    @classmethod
    def resolve(cls, strategy_name: str):
        if strategy_name == "default":
            return DefaultAllocationStrategy
