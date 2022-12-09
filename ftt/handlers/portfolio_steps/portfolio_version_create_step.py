from result import Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionCreateStep(AbstractStep):
    key = "portfolio_version"

    @classmethod
    def process(
        cls,
        version: int,
        portfolio_version: schemas.PortfolioVersion,
    ) -> Result[PortfolioVersion, str]:
        portfolio_version.version = version
        result = PortfolioVersionsRepository.create(portfolio_version=portfolio_version)
        return result
