from typing import Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Portfolio
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionNextVersionCalculationStep(AbstractStep):
    key = "next_version"

    @classmethod
    def process(cls, portfolio: Portfolio) -> Result[int, Optional[str]]:
        result = PortfolioVersionsRepository.get_latest_version(portfolio.id)

        if result is None:
            return Ok(1)
        else:
            return Ok(result.version + 1)
