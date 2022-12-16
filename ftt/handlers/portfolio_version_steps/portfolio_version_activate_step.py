from typing import Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
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
        cls, portfolio_version: schemas.PortfolioVersion
    ) -> Result[schemas.PortfolioVersion, Optional[str]]:
        portfolio_version.active = True
        result = PortfolioVersionsRepository.save(portfolio_version)
        return Ok(result)
