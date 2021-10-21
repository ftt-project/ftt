from typing import Optional

from result import Err, Ok, OkErr

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models.portfolio import Portfolio
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.repositories.portfolio_versions_repository import (
    PortfolioVersionsRepository,
)
from ftt.storage.repositories.securities_repository import SecuritiesRepository


class PortfolioSecuritiesLoadStep(AbstractStep):
    key = "securities"

    @classmethod
    def process(
        cls, portfolio: Portfolio, portfolio_version: Optional[PortfolioVersion] = None
    ) -> OkErr:
        if portfolio_version is None:
            portfolio_version = PortfolioVersionsRepository.get_latest_version(
                portfolio_id=portfolio.id
            )
        securities = SecuritiesRepository.find_securities(portfolio_version)

        if len(securities) == 0:
            return Err(f"No securities in portfolio {portfolio}")

        return Ok(securities)
