from typing import List, Optional

import pandas as pd
from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import Storage
from ftt.storage.models import PortfolioVersion
from ftt.storage.models.security import Security
from ftt.storage.models.security_price import SecurityPrice


class SecurityPricesDataframeLoadStep(AbstractStep):
    """
    Used to load security prices dataframe from storage.
    """

    key = "security_prices"

    @classmethod
    def process(
        cls,
        portfolio_version: PortfolioVersion,  # I don't like that it loads and version and securities, feels redundant
        portfolio_version_securities: List[Security],
    ) -> Result[pd.DataFrame, Optional[str]]:
        start_period = portfolio_version.period_start
        end_period = portfolio_version.period_end
        interval = portfolio_version.interval

        dataframes = []
        for security in portfolio_version_securities:
            query, params = (
                SecurityPrice.select(
                    SecurityPrice.datetime,
                    SecurityPrice.close,
                )
                .where(
                    SecurityPrice.interval == interval,
                    SecurityPrice.datetime >= start_period,
                    SecurityPrice.datetime <= end_period,
                    SecurityPrice.security == security,
                )
                .order_by(SecurityPrice.datetime.asc())
                .join(Security)
                .sql()
            )
            dataframe = pd.read_sql(
                query, Storage.get_database(), params=params, index_col="datetime"
            )

            df = pd.DataFrame({security.symbol: dataframe.close}, index=dataframe.index)
            df.index = pd.to_datetime(df.index)
            dataframes.append(df)

        dataframe = pd.concat(dataframes, axis=1).dropna()

        return Ok(dataframe)
