from typing import Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.portfolio_management.allocation_strategies import AllocationStrategyResolver
from ftt.portfolio_management.dtos import PortfolioAllocationDTO
from ftt.storage import schemas


class PortfolioVersionAllocationStep(AbstractStep):
    key = "portfolio_version_allocation"

    @classmethod
    def process(
        cls,
        optimization_result: PortfolioAllocationDTO,
        portfolio_version: schemas.PortfolioVersion,
        portfolio: schemas.Portfolio,
        security_prices,
    ) -> Result[PortfolioAllocationDTO, Optional[str]]:
        latest_prices = {k: v[-1] for k, v in security_prices.prices.items()}
        allocation_strategy = cls.__resolve_optimization_strategy(
            portfolio_version.allocation_strategy_name
        )

        result = allocation_strategy(
            allocation_dto=optimization_result,
            value=portfolio.value,
            latest_prices=latest_prices,
        ).allocate()

        return Ok(result)

    @classmethod
    def __resolve_optimization_strategy(cls, allocation_strategy_name):
        return AllocationStrategyResolver.resolve(
            strategy_name=allocation_strategy_name
        )
