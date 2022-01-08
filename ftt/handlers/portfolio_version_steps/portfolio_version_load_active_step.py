from typing import Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Portfolio, PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionLoadActiveStep(AbstractStep):
    key = "active_portfolio_version"

    @classmethod
    def process(
        cls, portfolio: Portfolio
    ) -> Result[Optional[PortfolioVersion], Optional[str]]:
        version = PortfolioVersionsRepository.get_active_version(portfolio)

        return Ok(version)
