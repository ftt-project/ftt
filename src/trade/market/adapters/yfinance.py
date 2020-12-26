import yfinance as yf

from src.trade.market.adapters.basic import Basic
from src.trade.market.quote import Quote


class Adapter(Basic):
    @classmethod
    def get_quote(cls, symbol):
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="10m", interval="1m")
        rows, columns = data.shape
        latest = data.iloc[rows - 1]
        return cls.__map_ticker_to_quote(ticker, latest, cls.__change(data, rows))

    @classmethod
    def get_quotes(cls, symbols_collection):
        symbols = " ".join(symbols_collection)
        tickers = yf.Tickers(symbols)
        quotes = []
        for ticker in tickers.tickers:
            data = ticker.history()
            rows, columns = data.shape
            latest = data.iloc[rows - 1]
            quote = cls.__map_ticker_to_quote(
                ticker,
                latest,
                cls.__change(data, rows),
                cls.__change_percent(data, rows),
            )
            quotes.append(quote)

        return quotes

    @classmethod
    def __map_ticker_to_quote(cls, ticker, data, change=None, change_percent=None):
        quote = Quote(
            symbol=ticker.ticker,
            open=data.get("Open"),
            high=data.get("High"),
            low=data.get("Low"),
            close=data.get("Close"),
            volume=data.get("Volume"),
            change=change,
            change_percent=change_percent,
        )
        return quote

    @classmethod
    def __change(cls, collection, rows):
        last = collection.iloc[rows - 1]
        before_last = collection.iloc[rows - 2]
        change = before_last.get("Close") - last.get("Close")
        return round(change, 2)

    @classmethod
    def __change_percent(cls, collection, rows):
        last = collection.iloc[rows - 1]
        absolute_change = cls.__change(collection, rows)
        change = absolute_change / last.get("Close") * 100
        return round(change, 2)
