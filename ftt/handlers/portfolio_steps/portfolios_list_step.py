from typing import Any

from result import Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfoliosListStep(AbstractStep):
    key = "list"

    @classmethod
    def process(cls):
        result = PortfoliosRepository.list()
        return Ok(list(result))
