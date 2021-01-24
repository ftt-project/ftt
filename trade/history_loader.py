from db.configuration import database_connection
from db.models import TickerReturn, Ticker
from trade.pandas_data import PandasData

import pandas as pd


class HistoryLoader:
    @staticmethod
    def load(ticker, interval="1m"):
        query = (
            TickerReturn.select(
                TickerReturn.datetime,
                TickerReturn.open,
                TickerReturn.high,
                TickerReturn.low,
                TickerReturn.close,
                TickerReturn.volume,
            )
            .where(
                TickerReturn.ticker == Ticker.get(Ticker.ticker == ticker),
                TickerReturn.interval == interval,
            )
            .order_by(TickerReturn.datetime.asc())
        )

        dataframe = pd.read_sql(
            query.sql()[0],
            database_connection(),
            params=query.sql()[1],
            # index_col="datetime",
        )
        dataframe["pct"] = dataframe.close.pct_change(1)
        dataframe["pct2"] = dataframe.close.pct_change(5)
        dataframe["pct3"] = dataframe.close.pct_change(10)

        return PandasData(dataname=dataframe)