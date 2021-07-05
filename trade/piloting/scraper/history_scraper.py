import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr


class HistoryScraper:
    @staticmethod
    def load(config) -> pd.DataFrame:
        """
        Loading tickers information from Yahoo
        """
        yf.pdr_override()
        data = pdr.get_data_yahoo(
            config.tickers,
            start=config.interval_start,
            end=config.interval_end,
            interval=config.interval,
        )
        return data
