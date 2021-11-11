from result import OkErr, Err, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.errors import PersistingError
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)


class PortfolioVersionUpdateStep(AbstractStep):
    key = "updated_portfolio_version"

    @classmethod
    def process(cls, portfolio_version: PortfolioVersion, params: dict) -> OkErr:
        try:
            result = PortfolioVersionsRepository.update(portfolio_version, params)
        except PersistingError as e:
            return Err(str(e))

        return Ok(result)
