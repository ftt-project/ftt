from typing import List, Optional

from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Security
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class PortfolioSecuritiesLoadStep(AbstractStep):
    """
    TODO: deprecate and remove
    """

    key = "securities"

    @classmethod
    def process(
        cls, portfolio_version: PortfolioVersion
    ) -> Result[List[Security], Optional[str]]:
        securities = SecuritiesRepository.find_securities(portfolio_version)

        if len(securities) == 0:
            return Err(
                f"No securities associated with portfolio version {portfolio_version.id}"
            )

        return Ok(securities)
