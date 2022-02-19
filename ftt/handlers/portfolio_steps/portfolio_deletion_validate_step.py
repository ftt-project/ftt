from typing import Optional

from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Portfolio
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioDeletionValidateStep(AbstractStep):
    key = "portfolio_deletion_validate"

    @classmethod
    def process(cls, portfolio: Portfolio) -> Result[Portfolio, Optional[str]]:
        active_portfolio_version = PortfolioVersionsRepository.get_active_version(
            portfolio
        )

        if active_portfolio_version is not None:
            return Err(
                f"Failed to delete Portfolio. Portfolio Version #{portfolio.id} is active."
            )
        else:
            return Ok(active_portfolio_version)
