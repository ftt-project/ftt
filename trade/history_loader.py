from trade.db.setup import database_connection

from trade.db.ticker_return import TickerReturn
from trade.pandas_data import PandasData

import pandas as pd


class HistoryLoader:
    """
    Loading tickers data from database
    """

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

    @staticmethod
    def load_multiple(tickers, interval):
        collection = {}
        for ticker in tickers:
            collection[ticker] = HistoryLoader.load(ticker, interval)
        return collection
