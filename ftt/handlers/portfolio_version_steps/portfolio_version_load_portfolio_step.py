from result import OkErr, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionLoadPortfolioStep(AbstractStep):
    key = "portfolio"

    @classmethod
    def process(cls, portfolio_version: PortfolioVersion) -> OkErr:
        result = PortfolioVersionsRepository.get_portfolio(
            portfolio_version_id=portfolio_version.id,
        )

        return Ok(result)
