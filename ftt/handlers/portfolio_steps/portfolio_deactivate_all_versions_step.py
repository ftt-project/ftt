from result import OkErr, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Portfolio
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioDeactivateAllVersionsStep(AbstractStep):
    key = "deactivated_portfolio_versions"

    @classmethod
    def process(cls, portfolio: Portfolio) -> OkErr:
        versions = PortfolioVersionsRepository.get_all_by_portfolio(portfolio)

        for version in versions:
            version.active = False
            PortfolioVersionsRepository.save(version)

        return Ok(versions)