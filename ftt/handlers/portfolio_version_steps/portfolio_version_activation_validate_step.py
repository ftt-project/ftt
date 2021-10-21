from result import OkErr, Ok, Err

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionActivationValidateStep(AbstractStep):
    key = "portfolio_version_activation_validation"

    @classmethod
    def process(cls, portfolio_version: PortfolioVersion) -> OkErr:
        version = PortfolioVersionsRepository.get_active_version(
            portfolio_version.portfolio
        )

        if version != portfolio_version:
            return Ok(portfolio_version)
        else:
            return Err(f"Portfolio Version #{portfolio_version.id} is already active")
