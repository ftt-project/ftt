from typing import List

from result import Ok, OkErr

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.portfolio_management import PortfolioAllocationDTO
from ftt.storage.data_objects.security_dto import SecurityDTO


class PortfolioPrepareEmptyWeightsStep(AbstractStep):
    key = "portfolio_version_allocation"

    @classmethod
    def process(cls, securities: List[SecurityDTO]) -> OkErr:
        result = dict(
            zip([security.symbol for security in securities], [0 for _ in securities])
        )
        allocation_dto = PortfolioAllocationDTO(
            weights=result,
            allocation=result,
            leftover=0,
            expected_annual_return=0,
            annual_volatility=0,
            sharpe_ratio=0,
        )
        return Ok(allocation_dto)
