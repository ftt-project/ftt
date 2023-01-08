from typing import List, Union, Optional

import yfinance as yf
from pandas_datareader import data as pdr
from result import Err, Ok, Result, as_result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.repositories.security_prices_repository import SecurityPricesRepository
from ftt.storage.value_objects import PortfolioVersionValueObject
from ftt.storage.models import PortfolioVersion
from ftt.storage.models.security import Security


class SecurityPricesDownloadStep(AbstractStep):
    """
    Downloads security prices from external source.
    Accepts list of securities and portfolio version. Portfolio Veri
    """
    key = "security_prices_data"

    @classmethod
    def process(
        cls,
        securities: list[schemas.Security],
        portfolio: schemas.Portfolio,
        mode: str = "always",
    ) -> Result[dict, Optional[str]]:
        if mode not in ["always", "on_missing"]:
            return Err(f"Unknown mode {mode}. Could be only 'always' or 'on_missing'")

        if mode == "on_missing":
            shapes = set()
            for security in securities:
                security_price_time_vector = as_result(Exception)(SecurityPricesRepository.security_price_time_vector)
                prices_result = security_price_time_vector(
                    security=security,
                    interval=portfolio.interval,
                    period_start=portfolio.period_start,
                    period_end=portfolio.period_end,
                )
                if prices_result.is_err():
                    return prices_result

                shapes.add(len(prices_result.value))
            if len(shapes) == 1 and shapes.pop() > 0:
                return Ok({})

        yf.pdr_override()
        symbols = [security.symbol for security in securities]
        try:
            dataframes = pdr.get_data_yahoo(
                symbols,
                start=portfolio.period_start,
                end=portfolio.period_end,
                interval=portfolio.interval,
            ).dropna()
            if len(securities) == 1:
                data = {securities[0].symbol: dataframes}
            else:
                data = {
                    idx: dataframes.xs(idx, level=1, axis=1)
                    for idx, gp in dataframes.groupby(level=1, axis=1)
                }

            return Ok(data)
        except Exception as e:
            return Err(str(e))
