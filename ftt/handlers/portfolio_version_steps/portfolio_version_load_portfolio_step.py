from typing import Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion, Portfolio
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionLoadPortfolioStep(AbstractStep):
    key = "portfolio"

    @classmethod
    def process(
        cls, portfolio_version: PortfolioVersion
    ) -> Result[Portfolio, Optional[str]]:
        result = PortfolioVersionsRepository.get_portfolio(
            portfolio_version_id=portfolio_version.id,
        )

        return Ok(result)
