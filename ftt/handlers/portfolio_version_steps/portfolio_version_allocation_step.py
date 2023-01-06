from typing import Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.portfolio_management.allocation_strategies import AllocationStrategyResolver
from ftt.storage.schemas import PortfolioAllocation
from ftt.storage import schemas


class PortfolioVersionAllocationStep(AbstractStep):
    key = "portfolio_version_allocation"

    @classmethod
    def process(
        cls,
        optimization_result: schemas.PortfolioAllocation,
        portfolio_version: schemas.PortfolioVersion,
        portfolio: schemas.Portfolio,
        security_prices: list[schemas.SecurityPricesTimeVector],
    ) -> Result[PortfolioAllocation, Optional[str]]:
        latest_prices = {
            security_price.security.symbol: security_price.prices[-1]
            for security_price in security_prices
        }
        allocation_strategy = cls.__resolve_optimization_strategy(
            portfolio_version.allocation_strategy_name
        )

        result = allocation_strategy(
            portfolio_allocation=optimization_result,
            value=portfolio.value,
            latest_prices=latest_prices,
        ).allocate()

        return Ok(result)

    @classmethod
    def __resolve_optimization_strategy(cls, allocation_strategy_name):
        return AllocationStrategyResolver.resolve(
            strategy_name=allocation_strategy_name
        )
