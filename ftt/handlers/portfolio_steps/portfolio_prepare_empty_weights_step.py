from typing import List, Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.schemas import PortfolioAllocation
from ftt.storage.value_objects import SecurityValueObject


class PortfolioPrepareEmptyWeightsStep(AbstractStep):
    key = "portfolio_version_allocation"

    @classmethod
    def process(
        cls, securities: List[SecurityValueObject]
    ) -> Result[PortfolioAllocation, Optional[str]]:
        result = dict(
            zip([security.symbol for security in securities], [0.0 for _ in securities])
        )
        allocation_dto = PortfolioAllocation(
            weights=result,
            allocation=result,
            leftover=0,
            expected_annual_return=0,
            annual_volatility=0,
            sharpe_ratio=0,
        )
        return Ok(allocation_dto)
