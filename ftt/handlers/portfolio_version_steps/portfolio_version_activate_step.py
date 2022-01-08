from typing import Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionActivateStep(AbstractStep):
    """
    Activates a portfolio version
    """

    key = "portfolio_version"

    @classmethod
    def process(
        cls, portfolio_version: PortfolioVersion
    ) -> Result[PortfolioVersion, Optional[str]]:
        portfolio_version.active = True
        result = PortfolioVersionsRepository.save(portfolio_version)
        return Ok(result)
