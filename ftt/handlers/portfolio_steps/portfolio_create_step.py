from result import Err, Ok, OkErr

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfolioCreateStep(AbstractStep):
    key = "portfolio"

    @classmethod
    def process(cls, name: str) -> OkErr:
        result = PortfoliosRepository.create(name=name)

        if result.id is not None:
            return Ok(result)
        else:
            return Err(result)
