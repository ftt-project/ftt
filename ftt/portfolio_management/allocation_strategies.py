import pandas as pd
from pypfopt import DiscreteAllocation
from pypfopt.base_optimizer import BaseOptimizer, portfolio_performance

from ftt.portfolio_management import PortfolioAllocationDTO


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

        if (
            self.allocation_dto.expected_annual_return is not None
            and self.allocation_dto.expected_annual_return != mu
        ):
            raise ValueError(
                "Expected annual return is already set "
                f"{self.allocation_dto.expected_annual_return} does not match actual {mu}"
            )
        self.allocation_dto.expected_annual_return = mu

        if (
            self.allocation_dto.annual_volatility is not None
            and self.allocation_dto.annual_volatility != sigma
        ):
            raise ValueError(
                "Expected volatility is already set "
                f"{self.allocation_dto.annual_volatility} does not match actual {sigma}"
            )
        self.allocation_dto.annual_volatility = sigma

        self.allocation_dto.allocation = pd.Series(
            index=weights.keys(), data=alloc.values()
        ).to_dict()
        self.allocation_dto.leftover = leftover

        return self.allocation_dto
