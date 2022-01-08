from typing import Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionDeactivateStep(AbstractStep):
    """
    Deactivate a portfolio version.
    """

    key = "deactivated_portfolio_version"

    @classmethod
    def process(
        cls, portfolio_version: Optional[PortfolioVersion]
    ) -> Result[PortfolioVersion, Optional[str]]:
        if not portfolio_version:
            return Ok()

        portfolio_version.active = False
        result = PortfolioVersionsRepository.save(portfolio_version)
        return Ok(result)
