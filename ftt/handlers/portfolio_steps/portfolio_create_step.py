from typing import Optional

from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Portfolio
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfolioCreateStep(AbstractStep):
    key = "portfolio"

    @classmethod
    def process(cls, name: str) -> Result[Portfolio, Optional[str]]:
        result = PortfoliosRepository.create(name=name)

        if result.id is not None:
            return Ok(result)
        else:
            return Err(result)
