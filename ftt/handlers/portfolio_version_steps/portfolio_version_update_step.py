from typing import Optional

from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.value_objects import PortfolioVersionValueObject
from ftt.storage.errors import PersistingError
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionUpdateStep(AbstractStep):
    key = "updated_portfolio_version"

    @classmethod
    def process(
        cls, portfolio_version: PortfolioVersion, dto: PortfolioVersionValueObject
    ) -> Result[PortfolioVersion, Optional[str]]:
        try:
            result = PortfolioVersionsRepository.update(portfolio_version, dto)
        except PersistingError as e:
            return Err(str(e))

        return Ok(result)
