from typing import List, Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Portfolio, PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionsListStep(AbstractStep):
    key = "portfolio_versions"

    @classmethod
    def process(
        cls, portfolio: Portfolio
    ) -> Result[List[PortfolioVersion], Optional[str]]:
        versions = PortfolioVersionsRepository.get_all_by_portfolio(portfolio)

        return Ok(versions)
