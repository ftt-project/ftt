from typing import Optional

from result import as_result, Result, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Portfolio
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfolioUpdateStep(AbstractStep):
    key = "updated_portfolio"

    @classmethod
    def process(
        cls,
        portfolio: Portfolio,
    ) -> Result[Portfolio, Optional[str]]:
        update = as_result(Exception)(PortfoliosRepository.update)
        result = update(portfolio)

        return Ok(result.unwrap())
