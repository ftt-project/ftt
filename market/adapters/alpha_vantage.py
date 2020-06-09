from alpha_vantage.timeseries import TimeSeries

from market.qoute import Qoute

class Adapter:
    key = 'KHRYFWCSGMXTXR9U'

    @classmethod
    def get_quote(cls, symbol):
        ts = TimeSeries(key=cls.key)
        answer, metadata = ts.get_quote_endpoint(symbol)
        qoute = Qoute(
            symbol=answer['01. symbol'],
            open=float(answer['02. open']),
            high=float(answer['03. high']),
            low=float(answer['04. low']),
            price=float(answer['05. price']),
            volume=int(answer['06. volume']),
            change=float(answer['09. change']),
            change_percent=float(answer['10. change percent'].strip('%'))
        )
        return qoute
