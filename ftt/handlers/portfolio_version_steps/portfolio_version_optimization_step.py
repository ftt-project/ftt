from typing import Optional

import pandas as pd
from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.portfolio_management.optimization_strategies import (
    OptimizationStrategyResolver,
    AbstractOptimizationStrategy,
)
from ftt.storage.data_objects.portfolio_security_prices_range_dto import (
    PortfolioSecurityPricesRangeDTO,
)
from ftt.storage.models import PortfolioVersion


class PortfolioVersionOptimizationStep(AbstractStep):
    key = "optimization_result"

    @classmethod
    def process(
        cls,
        optimization_strategy_name: str,
        portfolio_version: PortfolioVersion,
        security_prices: PortfolioSecurityPricesRangeDTO,
    ) -> Result[AbstractOptimizationStrategy, Optional[str]]:
        returns = pd.DataFrame(
            data=security_prices.prices,
            index=pd.to_datetime(security_prices.datetime_list),
        )
        optimization_strategy = cls.__resolve_optimization_strategy(
            optimization_strategy_name
        )
        result = optimization_strategy(returns=returns).optimize()

        return Ok(result)

    @classmethod
    def __resolve_optimization_strategy(cls, optimization_strategy):
        return OptimizationStrategyResolver.resolve(strategy_name=optimization_strategy)
