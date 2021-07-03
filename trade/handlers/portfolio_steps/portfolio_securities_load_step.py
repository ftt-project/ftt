from typing import Optional

from result import Err, Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models import Portfolio, PortfolioVersion
from trade.storage.repositories import PortfolioVersionsRepository, SecuritiesRepository


class PortfolioSecuritiesLoadStep(AbstractStep):
    key = "securities"

    @classmethod
    def process(
        cls, portfolio: Portfolio, version: Optional[PortfolioVersion] = None
    ) -> OkErr:
        if version is None:
            version = PortfolioVersionsRepository.get_latest_version(
                portfolio_id=portfolio.id
            )
        securities = SecuritiesRepository.find_securities(version)

        if len(securities) == 0:
            return Err(f"No securities in portfolio {portfolio}")

        return Ok(securities)
