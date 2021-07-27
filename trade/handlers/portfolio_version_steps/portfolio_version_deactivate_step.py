from typing import Optional

from result import Ok

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models import PortfolioVersion
from trade.storage.repositories.portfolio_versions_repository import PortfolioVersionsRepository


class PortfolioVersionDeactivateStep(AbstractStep):
    key = "deactivated_portfolio_version"

    @classmethod
    def process(cls, active_portfolio_version: Optional[PortfolioVersion]):
        if not active_portfolio_version:
            return Ok()

        active_portfolio_version.active = False
        result = PortfolioVersionsRepository.save(active_portfolio_version)
        return Ok(result)
