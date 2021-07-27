from result import OkErr, Ok

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models import PortfolioVersion
from trade.storage.repositories.portfolio_versions_repository import PortfolioVersionsRepository


class PortfolioVersionActivateStep(AbstractStep):
    key = "portfolio_version"

    @classmethod
    def process(cls, portfolio_version: PortfolioVersion) -> OkErr:
        portfolio_version.active = True
        result = PortfolioVersionsRepository.save(portfolio_version)
        return Ok(result)
