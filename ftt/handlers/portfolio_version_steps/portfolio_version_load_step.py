from typing import Optional

import peewee
from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionLoadStep(AbstractStep):
    """
    Loads portfolio_management version from database by its ID
    """

    key = "portfolio_version"

    @classmethod
    def process(
        cls, portfolio_version_id: int
    ) -> Result[PortfolioVersion, Optional[str]]:
        try:
            # TODO: peewee exception handling must be moved to the repository level
            found = PortfolioVersionsRepository.get_by_id(portfolio_version_id)
        except peewee.DoesNotExist:
            return Err(
                f"Portfolio Version with ID {portfolio_version_id} does not exist"
            )

        return Ok(found)
