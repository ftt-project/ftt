from datetime import datetime
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
        securities = cls.__load_securities(portfolio_version)
        if len(securities) == 0:
            return Err(
                f"No securities associated with portfolio version {portfolio_version.id}"
            )

        prices = {}
        datetime_list: list[datetime] = []
        for security in securities:
            security_prices = cls.__load_prices(security, portfolio_version)
            prices[security.symbol] = [float(price.close) for price in security_prices]

            if not datetime_list:
                datetime_list = [price.datetime for price in security_prices]

        shapes = {
            security_symbol: len(price) for security_symbol, price in prices.items()
        }
        if len(set(shapes.values())) > 1:
            return Err(f"Data points shapes do not match: {shapes}")

        dto = PortfolioSecurityPricesRangeDTO(
            prices=prices, datetime_list=datetime_list
        )

        return Ok(dto)

    @staticmethod
    def __load_securities(portfolio_version):
        return SecuritiesRepository.find_securities(portfolio_version=portfolio_version)

    @staticmethod
    def __load_prices(security, portfolio_version):
        return SecurityPricesRepository.find_by_security_prices(
            security=security,
            interval=portfolio_version.interval,
            period_start=portfolio_version.period_start,
            period_end=portfolio_version.period_end,
        )
