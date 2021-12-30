import peewee
from result import Err, Ok, OkErr

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfolioLoadStep(AbstractStep):
    key = "portfolio"

    @classmethod
    def process(cls, portfolio_id: int) -> OkErr:
        try:
            result = PortfoliosRepository.get_by_id(portfolio_id)
        # TODO move exception handling to the level of repository
        except peewee.DoesNotExist:
            return Err(f"Portfolio with ID {portfolio_id} does not exist")

        return Ok(result)
