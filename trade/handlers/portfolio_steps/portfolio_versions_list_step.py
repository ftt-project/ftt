from result import Ok

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models import Portfolio
from trade.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionsListStep(AbstractStep):
    key = "portfolio_versions"

    @classmethod
    def process(cls, portfolio: Portfolio):
        versions = PortfolioVersionsRepository.get_all_by_portfolio(portfolio)

        return Ok(versions)
