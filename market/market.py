from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

from .qoute import Qoute

class Market(object):
    key = 'KHRYFWCSGMXTXR9U'

    @classmethod
    def get_quote_endpoint(cls, symbol):
        '''Return Qoute object with current price, volume and stats of the symbol'''
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
