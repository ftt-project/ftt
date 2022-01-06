from typing import Optional

from result import Ok, Err, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects import DTOInterface
from ftt.storage.errors import PersistingError
from ftt.storage.models import Portfolio
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfolioUpdateStep(AbstractStep):
    key = "updated_portfolio"

    @classmethod
    def process(
        cls, portfolio: Portfolio, dto: DTOInterface
    ) -> Result[Portfolio, Optional[str]]:
        try:
            result = PortfoliosRepository.update(portfolio, dto)
        except PersistingError as e:
            return Err(str(e))

        return Ok(result)
