from result import Err, Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models.portfolio import Portfolio
from trade.storage.repositories.portfolio_versions_repository import PortfolioVersionsRepository


class PortfolioVersionCreateStep(AbstractStep):
    key = "portfolio_version"

    @classmethod
    def process(cls, version: int, portfolio: Portfolio) -> OkErr:
        result = PortfolioVersionsRepository.create(
            version=version, portfolio_id=portfolio.id
        )
        if result.id is not None:
            return Ok(result)
        else:
            return Err(result)
