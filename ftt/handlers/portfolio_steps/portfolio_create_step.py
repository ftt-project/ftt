from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfolioCreateStep(AbstractStep):
    key = "portfolio"

    @classmethod
    def process(cls, portfolio: schemas.Portfolio) -> Result[schemas.Portfolio, str]:
        result = PortfoliosRepository.create(portfolio)

        if result.id is not None:
            return Ok(result)
        else:
            return Err(f"Failed to create portfolio: {result}")
