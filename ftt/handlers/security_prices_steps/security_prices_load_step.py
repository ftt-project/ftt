from typing import Optional

from result import Ok, Err, Result, as_result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.repositories.portfolio_security_repository import (
    PortfolioSecurityRepository,
)
from ftt.storage.repositories.security_prices_repository import SecurityPricesRepository


class SecurityPricesLoadStep(AbstractStep):
    """
    Loads security prices for a given portfolio version.

    Params:
    -------
        portfolio_version: schemas.PortfolioVersion - Portfolio version to load security prices for.
        portfolio: schemas.Portfolio - Portfolio to load security prices for.
            Used to load securities associated with the portfolio.


    Returns:
    --------
        Result[List[schemas.SecurityPricesTimeVector], Optional[str]] - Result with list of security prices bound
            to timeline, and error message if any.
    """

    key = "security_prices"

    @classmethod
    def process(
        cls, portfolio: schemas.Portfolio
    ) -> Result[list[schemas.SecurityPricesTimeVector], Optional[str]]:
        list_all = as_result(Exception)(PortfolioSecurityRepository.list)
        securities_result = list_all(portfolio=portfolio)

        match securities_result:
            case Ok(s):
                if len(s) == 0:
                    return Err(
                        f"No securities associated with portfolio {portfolio.id}"
                    )
            case Err(err):
                return Err(err)

        securities: list[schemas.PortfolioSecurity] = [
            ps.security for ps in securities_result.unwrap()
        ]

        prices = []
        security_price_time_vector = as_result(Exception)(
            SecurityPricesRepository.security_price_time_vector
        )
        for security in securities:
            security_prices_result = security_price_time_vector(
                security=security,
                interval=portfolio.interval,
                period_start=portfolio.period_start,
                period_end=portfolio.period_end,
            )

            if security_prices_result.is_err():
                return Err(security_prices_result.unwrap_err())

            security_prices = security_prices_result.unwrap()

            prices_time_vector = schemas.SecurityPricesTimeVector(
                security=security,
                prices=[sp.close for sp in security_prices],
                time_vector=[price.datetime for price in security_prices],
            )
            prices.append(prices_time_vector)

        shapes = {
            security_price_vector.security.symbol: len(security_price_vector.prices)
            for security_price_vector in prices
        }
        if len(set(shapes.values())) > 1:
            return Err(f"Data points shapes do not match: {shapes}")

        return Ok(prices)
