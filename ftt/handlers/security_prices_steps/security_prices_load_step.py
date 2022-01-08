from typing import Optional

from result import Ok, Err, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects.portfolio_security_prices_range_dto import (
    PortfolioSecurityPricesRangeDTO,
)
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.securities_repository import SecuritiesRepository
from ftt.storage.repositories.security_prices_repository import SecurityPricesRepository


class SecurityPricesLoadStep(AbstractStep):
    key = "security_prices"

    @classmethod
    def process(
        cls, portfolio_version: PortfolioVersion
    ) -> Result[PortfolioSecurityPricesRangeDTO, Optional[str]]:
        securities = SecuritiesRepository.find_securities(
            portfolio_version=portfolio_version
        )
        if len(securities) == 0:
            return Err(
                f"No securities associated with portfolio version {portfolio_version.id}"
            )

        prices = {}
        datetime_list = None
        for security in securities:
            security_prices = SecurityPricesRepository.find_by_security_prices(
                security=security,
                interval=portfolio_version.interval,
                period_start=portfolio_version.period_start,
                period_end=portfolio_version.period_end,
            )
            if datetime_list is None:
                datetime_list = [price.datetime for price in security_prices]
            prices[security.symbol] = [float(price.close) for price in security_prices]

        dto = PortfolioSecurityPricesRangeDTO(
            prices=prices, datetime_list=datetime_list
        )

        return Ok(dto)
