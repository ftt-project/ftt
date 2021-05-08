from collections import OrderedDict
from datetime import date

from trade.models import Ticker
from trade.models import database_connection

from trade.models.ticker_return import TickerReturn
from trade.pandas_data import PandasData

import pandas as pd


class HistoryLoader:
    """
    Loading tickers data from database
    """

    @staticmethod
    def load(ticker: str, start_date: date, end_date: date,  interval: str = "1m") -> PandasData:
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
                TickerReturn.symbol == Ticker.get(Ticker.symbol == ticker),
                TickerReturn.interval == interval,
                ((TickerReturn.datetime >= start_date) | (TickerReturn.datetime <= end_date))
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
    def load_multiple(tickers: dict, start_date: date, end_date: date, interval: str) -> dict:
        collection = {}
        for ticker in tickers:
            collection[ticker] = HistoryLoader.load(ticker, start_date, end_date, interval)
        return OrderedDict(sorted(collection.items()))
