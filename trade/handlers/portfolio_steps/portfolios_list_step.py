from typing import Any

from result import Ok

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfoliosListStep(AbstractStep):
    key = "list"

    @classmethod
    def process(cls, *args: Any):
        result = PortfoliosRepository.list()
        return Ok(list(result))
