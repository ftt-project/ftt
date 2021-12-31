from result import OkErr, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.portfolio_management.dtos import PortfolioAllocationDTO
from ftt.storage.models import PortfolioVersion


class PortfolioVersionAllocationStep(AbstractStep):
    key = "portfolio_version_allocation"

    @classmethod
    def process(
        cls,
        optimization_result: PortfolioAllocationDTO,
        portfolio_version: PortfolioVersion,
        allocation_strategy,
        security_prices,
    ) -> OkErr:
        latest_prices = {k: v[-1] for k, v in security_prices.prices.items()}
        result = allocation_strategy(
            allocation_dto=optimization_result,
            value=portfolio_version.value,
            latest_prices=latest_prices,
        ).allocate()

        return Ok(result)
