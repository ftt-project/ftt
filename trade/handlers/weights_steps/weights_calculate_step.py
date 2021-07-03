from pandas import DataFrame
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import DiscreteAllocation
from result import Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep


class WeightsCalculateStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(cls, security_prices: DataFrame, portfolio_budget: float) -> OkErr:
        # returns = security_prices.pct_change().dropna()

        mu = expected_returns.return_model(security_prices, method="capm_return")
        S = risk_models.risk_matrix(security_prices, method="oracle_approximating")

        ef = EfficientFrontier(mu, S)

        raw_weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()

        ef.portfolio_performance(verbose=True)

        da = DiscreteAllocation(
            cleaned_weights,
            security_prices.iloc[-1],
            total_portfolio_value=portfolio_budget,
        )
        alloc, leftover = da.lp_portfolio()

        return Ok((alloc, leftover,))
