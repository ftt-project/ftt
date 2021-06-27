from typing import Any, Optional
from result import Ok, Err, OkErr

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models import Portfolio, PortfolioVersion
from trade.storage.repositories import PortfolioVersionsRepository, SecuritiesRepository


class PortfolioSecuritiesLoadStep(AbstractStep):
    key = "securities"

    @classmethod
    def process(cls, portfolio: Portfolio, version: Optional[PortfolioVersion] = None) -> OkErr:
        if version is None:
            version = PortfolioVersionsRepository.get_latest_version(portfolio_id=portfolio.id)
        securities = SecuritiesRepository.find_securities(version)

        return Ok(securities)
