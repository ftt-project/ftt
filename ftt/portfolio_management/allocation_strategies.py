import numpy as np
import pandas as pd

from ftt.portfolio_management.dtos import PortfolioAllocationDTO


class DefaultAllocationStrategy:
    def __init__(
        self,
        allocation_dto: PortfolioAllocationDTO,
        value: float,
        latest_prices: dict[str, float],
    ):
        self.allocation_dto = allocation_dto
        self.value = value
        self.latest_prices = pd.Series(latest_prices)

    def allocate(self):
        from pypfopt import DiscreteAllocation  # type: ignore
        from pypfopt.base_optimizer import BaseOptimizer, portfolio_performance  # type: ignore

        optimizer = BaseOptimizer(len(self.latest_prices))
        weights = pd.Series(self.allocation_dto.weights)
        optimizer.set_weights(weights)
        cleaned_weights = optimizer.clean_weights()

        mu, sigma, sharpe = portfolio_performance(
            weights, self.latest_prices, self.allocation_dto.cov_matrix
        )

        da = DiscreteAllocation(
            cleaned_weights,
            self.latest_prices,
            total_portfolio_value=float(self.value),
        )
        alloc, leftover = da.lp_portfolio()

        self.__set_expected_annual_return(mu)
        self.__set_annual_volatility(sigma)
        self.allocation_dto.allocation = self.__normalize_allocation(
            weights.keys().to_list(), alloc
        )
        self.allocation_dto.leftover = leftover

        return self.allocation_dto

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
            self.allocation_dto.expected_annual_return is not None
            and self.allocation_dto.expected_annual_return != mu
        ):
            raise ValueError(
                "Expected annual return is already set "
                f"{self.allocation_dto.expected_annual_return} does not match actual {mu}"
            )
        self.allocation_dto.expected_annual_return = mu

    def __set_annual_volatility(self, sigma):
        if (
            self.allocation_dto.annual_volatility is not None
            and self.allocation_dto.annual_volatility != sigma
        ):
            raise ValueError(
                "Expected volatility is already set "
                f"{self.allocation_dto.annual_volatility} does not match actual {sigma}"
            )
        self.allocation_dto.annual_volatility = sigma


class AllocationStrategyResolver:
    strategies = ["default"]

    @classmethod
    def resolve(cls, strategy_name: str):
        if strategy_name == "default":
            return DefaultAllocationStrategy
