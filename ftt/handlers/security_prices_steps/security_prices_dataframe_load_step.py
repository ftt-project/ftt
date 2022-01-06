from datetime import datetime
from typing import List, Optional

import pandas as pd
from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import Storage
from ftt.storage.models.security import Security
from ftt.storage.models.security_price import SecurityPrice


class SecurityPricesDataframeLoadStep(AbstractStep):
    """
    TODO: deprecate and remove
    """

    key = "security_prices"

    @classmethod
    def process(
        cls,
        securities: List[Security],
        start_period: datetime,
        end_period: datetime,
        interval: str,
    ) -> Result[pd.DataFrame, Optional[str]]:
        dataframes = []
        for security in securities:
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
            dataframes.append(df)

        dataframe = pd.concat(dataframes, axis=1).dropna()

        return Ok(dataframe)
