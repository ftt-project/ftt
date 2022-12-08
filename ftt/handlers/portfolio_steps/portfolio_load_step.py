from typing import Optional

import peewee
from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.models import Portfolio
from ftt.storage.repositories.portfolios_repository import PortfoliosRepository


class PortfolioLoadStep(AbstractStep):
    key = "portfolio"

    @classmethod
    def process(cls, portfolio: schemas.Portfolio) -> Result[schemas.Portfolio, str]:
        result = PortfoliosRepository.get_by_id(portfolio)
        if result is None:
            return Err(f"Portfolio with ID {portfolio.id} does not exist")

        return Ok(result)
