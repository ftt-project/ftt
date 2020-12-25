from pandas_datareader import data as pdr
import yfinance as yf


class HistoryScraper:
    @staticmethod
    def load(config):
        """
        Loading tickers information from Yahoo
        """
        yf.pdr_override()
        data = pdr.get_data_yahoo(
            config.tickers,
            start=config.interval_start,
            end=config.interval_end,
            interval=config.interval
        )
        print(data.head())
