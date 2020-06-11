import yfinance as yf

from src.trade.market.quote import Quote

class Adapter:
    @classmethod
    def get_quote(cls, symbol):
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='10m', interval='1m')
        rows, columns = data.shape
        latest = data.iloc[rows-1]
        quote = Quote(
            symbol=symbol,
            open=latest.get('Open'),
            high=latest.get('High'),
            low=latest.get('Low'),
            close=latest.get('Close'),
            volume=latest.get('Volume'),
            change=cls.change(data, rows),
            change_percent=None
        )
        return quote

    @classmethod
    def change(cls, collection, rows):
        last = collection.iloc[rows-1]
        before_last = collection.iloc[rows - 2]
        change = before_last.get('Close') - last.get('Close')
        return round(change, 2)