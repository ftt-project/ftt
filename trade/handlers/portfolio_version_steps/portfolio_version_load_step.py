import peewee
from result import OkErr, Ok, Err

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.repositories.portfolio_versions_repository import PortfolioVersionsRepository


class PortfolioVersionLoadStep(AbstractStep):
    key = "portfolio_version"

    @classmethod
    def process(cls, portfolio_version_id: int) -> OkErr:
        try:
            found = PortfolioVersionsRepository.get_by_id(portfolio_version_id)
        except peewee.DoesNotExist:
            return Err(f"Portfolio Version with ID {portfolio_version_id} does not exist")

        return Ok(found)
