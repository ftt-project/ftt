from typing import Optional, List

from result import Err, Ok, Result

from ftt.storage.models import PortfolioVersion, Security
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class PortfolioVersionLoadSecuritiesStep:
    key = "portfolio_version_securities"

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
