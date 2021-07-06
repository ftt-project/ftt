from pandas import DataFrame
from pypfopt import DiscreteAllocation, EfficientFrontier, expected_returns, risk_models
from result import Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models.portfolio import Portfolio


class WeightsCalculateStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(cls, security_prices: DataFrame, portfolio: Portfolio) -> OkErr:
        _ = security_prices.pct_change().dropna()

        mu = expected_returns.return_model(security_prices, method="capm_return")
        S = risk_models.risk_matrix(security_prices, method="oracle_approximating")

        ef = EfficientFrontier(mu, S)

        _ = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()

        # TODO: save performance into portfolio version
        # mu, sigma, sharpe = ef.portfolio_performance()
        _ = ef.portfolio_performance()

        da = DiscreteAllocation(
            cleaned_weights,
            security_prices.iloc[-1],
            total_portfolio_value=portfolio.amount,
        )
        alloc, leftover = da.lp_portfolio()

        return Ok((alloc, leftover,))
