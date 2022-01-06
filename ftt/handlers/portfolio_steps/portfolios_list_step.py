from typing import Optional, List

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Portfolio
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfoliosListStep(AbstractStep):
    key = "list"

    @classmethod
    def process(cls) -> Result[List[Portfolio], Optional[str]]:
        result = PortfoliosRepository.list()
        return Ok(list(result))
