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
            open=answer['02. open'],
            high=answer['03. high'],
            low=answer['04. low'],
            price=answer['05. price'],
            volume=answer['06. volume'],
            change=answer['09. change'],
            change_percent=answer['10. change percent']
        )
        return qoute
