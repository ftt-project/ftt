from typing import List, Union, Optional

import yfinance as yf
from pandas_datareader import data as pdr
from result import Err, Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO
from ftt.storage.models import PortfolioVersion
from ftt.storage.models.security import Security


class SecurityPricesDownloadStep(AbstractStep):
    key = "security_prices_data"

    @classmethod
    def process(
        cls,
        securities: List[Security],
        portfolio_version: Union[PortfolioVersionDTO, PortfolioVersion],
    ) -> Result[dict, Optional[str]]:
        yf.pdr_override()
        symbols = [security.symbol for security in securities]
        try:
            dataframes = pdr.get_data_yahoo(
                symbols,
                start=portfolio_version.period_start,
                end=portfolio_version.period_end,
                interval=portfolio_version.interval,
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
