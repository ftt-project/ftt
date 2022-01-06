from typing import Optional

import peewee
from result import Ok, Err, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion, Security
from ftt.storage.repositories.weights_repository import WeightsRepository


class WeightsDeleteStep(AbstractStep):
    key = "weights_delete"

    @classmethod
    def process(
        cls, portfolio_version: PortfolioVersion, securities: Security
    ) -> Result[bool, Optional[str]]:
        results = []
        for security in securities:
            try:
                result = WeightsRepository.find_by_security_and_portfolio(
                    portfolio_version_id=portfolio_version.id, security=security
                )
                WeightsRepository.delete(result)
            # TODO: move exception handler to repository level
            except peewee.DoesNotExist:
                results.append(
                    Err(
                        f"Weight {security.symbol} associated with portfolio version #{portfolio_version.id} not found"
                    )
                )

        if all([result.is_ok() for result in results]):
            return Ok(True)
        else:
            return Err("; ".join([result.value for result in results]))
