from typing import Optional

import pandas as pd
from result import Ok, Result, Err

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.portfolio_management.optimization_strategies import (
    OptimizationStrategyResolver,
    AbstractOptimizationStrategy,
)
from ftt.storage import schemas


class PortfolioVersionOptimizationStep(AbstractStep):
    key = "optimization_result"

    @classmethod
    def process(
        cls,
        portfolio_version: schemas.PortfolioVersion,
        security_prices: list[schemas.SecurityPricesTimeVector],
    ) -> Result[AbstractOptimizationStrategy, Optional[str]]:
        errors = []
        for security_price in security_prices:
            if not security_price.prices or not security_price.time_vector:
                errors.append(f"Prices for {security_price.security.symbol} are empty")

        if errors:
            return Err(". ".join(errors))

        returns = pd.DataFrame(
            data={sp.security.symbol: sp.prices for sp in security_prices},
            index=pd.to_datetime(security_prices[0].time_vector),
        )
        optimization_strategy = cls.__resolve_optimization_strategy(
            portfolio_version.optimization_strategy_name
        )
        result = optimization_strategy(returns=returns).optimize()

        return Ok(result)

    @classmethod
    def __resolve_optimization_strategy(cls, optimization_strategy):
        return OptimizationStrategyResolver.resolve(strategy_name=optimization_strategy)
