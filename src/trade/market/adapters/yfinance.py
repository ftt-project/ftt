import yfinance as yf

from src.trade.market.qoute import Qoute

class Adapter:
    @classmethod
    def get_quote(cls, symbol):
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d', interval='1d')
        rows, columns = data.shape
        latest = data.iloc[rows-1]
        qoute = Qoute(
            symbol=symbol,
            open=latest.get('Open'),
            high=latest.get('High'),
            low=latest.get('Low'),
            price=latest.get('Close'),
            volume=latest.get('Volume'),
            change=None,
            change_percent=None
        )
        return qoute
