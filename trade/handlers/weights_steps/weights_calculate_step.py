from dataclasses import dataclass

import pypfopt
from pandas import DataFrame
from pypfopt import DiscreteAllocation, EfficientFrontier, expected_returns, risk_models
from result import Ok, OkErr, Err

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models.portfolio import Portfolio


@dataclass(frozen=True)
class WeightsCalculateStepResult:
    allocation: dict[str, int]
    leftover: float
    expected_annual_return: float
    annual_volatility: float
    sharpe_ratio: float


class WeightsCalculateStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(cls, security_prices: DataFrame, portfolio: Portfolio) -> OkErr:
        try:
            _ = security_prices.pct_change().dropna()

            mu = expected_returns.return_model(security_prices, method="capm_return")
            S = risk_models.risk_matrix(security_prices, method="oracle_approximating")

            ef = EfficientFrontier(mu, S)

            _ = ef.max_sharpe()
            cleaned_weights = ef.clean_weights()

            mu, sigma, sharpe = ef.portfolio_performance()

            da = DiscreteAllocation(
                cleaned_weights,
                security_prices.iloc[-1],
                total_portfolio_value=portfolio.amount,
            )
            alloc, leftover = da.lp_portfolio()

            result = WeightsCalculateStepResult(alloc, leftover, mu, sigma, sharpe)

            return Ok(result)

        except pypfopt.exceptions.OptimizationError as e:
            return Err(' '.join(e.args))
