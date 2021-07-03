from datetime import datetime
from typing import Any, List

import pandas as pd
from result import Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep
from trade.storage import Storage
from trade.storage.models import Security, SecurityPrice


class SecurityPricesDataframeLoadStep(AbstractStep):
    key = "security_prices"

    @classmethod
    def process(
        cls,
        securities: List[Security],
        start_period: datetime,
        end_period: datetime,
        interval: str,
    ) -> OkErr:
        dataframes = []
        for security in securities:
            query, params = (
                SecurityPrice.select(SecurityPrice.datetime, SecurityPrice.close,)
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
