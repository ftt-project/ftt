from alpha_vantage.timeseries import TimeSeries

from src.trade.market.adapters.basic import Basic
from src.trade.market.quote import Quote


class Adapter(Basic):
    key = 'KHRYFWCSGMXTXR9U'

    @classmethod
    def get_quote(cls, symbol):
        ts = TimeSeries(key=cls.key)
        answer, metadata = ts.get_quote_endpoint(symbol)
        quote = Quote(
            symbol=answer['01. symbol'],
            open=float(answer['02. open']),
            high=float(answer['03. high']),
            low=float(answer['04. low']),
            close=float(answer['05. price']),
            volume=int(answer['06. volume']),
            change=float(answer['09. change']),
            change_percent=float(answer['10. change percent'].strip('%'))
        )
        return quote

    def get_quotes(self):
        pass
