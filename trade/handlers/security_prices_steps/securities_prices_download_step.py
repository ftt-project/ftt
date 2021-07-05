from datetime import datetime
from typing import List

import yfinance as yf
from pandas_datareader import data as pdr
from result import Err, Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage.models.security import Security


class SecurityPricesDownloadStep(AbstractStep):
    key = "security_prices_data"

    @classmethod
    def process(
        cls,
        securities: List[Security],
        period_from: datetime,
        period_to: datetime,
        interval: str,
    ) -> OkErr:
        yf.pdr_override()
        symbols = [security.symbol for security in securities]
        try:
            dataframes = pdr.get_data_yahoo(
                symbols, start=period_from, end=period_to, interval=interval,
            )
            if len(securities) == 1:
                data = {securities[0].symbol: dataframes}
            else:
                data = {
                    idx: dataframes.xs(idx, level=1, axis=1)
                    for idx, gp in dataframes.groupby(level=1, axis=1)
                }

            return Ok(data)
        except Exception as e:
            return Err(e)
