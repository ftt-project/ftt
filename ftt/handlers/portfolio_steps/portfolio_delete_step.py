from typing import Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Portfolio
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfolioDeleteStep(AbstractStep):
    key = "deleted_portfolio"

    @classmethod
    def process(cls, portfolio: Portfolio) -> Result[Portfolio, Optional[str]]:
        result = PortfoliosRepository.delete(portfolio)
        return Ok(result)
