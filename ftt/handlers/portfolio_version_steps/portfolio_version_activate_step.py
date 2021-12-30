from result import OkErr, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionActivateStep(AbstractStep):
    """
    Activates a portfolio_management version
    """

    key = "portfolio_version"

    @classmethod
    def process(cls, portfolio_version: PortfolioVersion) -> OkErr:
        portfolio_version.active = True
        result = PortfolioVersionsRepository.save(portfolio_version)
        return Ok(result)
