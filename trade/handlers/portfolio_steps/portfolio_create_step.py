from result import Err, Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfolioCreateStep(AbstractStep):
    key = "portfolio"

    @classmethod
    def process(cls, name: str, amount: float) -> OkErr:
        result = PortfoliosRepository.create(name=name, amount=amount)

        if result.id is not None:
            return Ok(result)
        else:
            return Err(result)