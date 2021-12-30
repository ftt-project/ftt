import pandas as pd
from result import OkErr, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects.portfolio_security_prices_range_dto import (
    PortfolioSecurityPricesRangeDTO,
)
from ftt.storage.models import PortfolioVersion


class PortfolioVersionOptimizationStep(AbstractStep):
    key = "optimization_result"

    @classmethod
    def process(
        cls,
        optimization_strategy,
        portfolio_version: PortfolioVersion,
        security_prices: PortfolioSecurityPricesRangeDTO,
    ) -> OkErr:
        returns = pd.DataFrame(
            data=security_prices.prices,
            index=pd.to_datetime(security_prices.datetime_list),
        )
        result = optimization_strategy(returns=returns).optimize()

        return Ok(result)
