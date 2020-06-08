from alpha_vantage.techindicators import TechIndicators

from market.adapters import alpha_vantage
from market.adapters import yfinance

class Market(object):
    def __init__(self, adapter=alpha_vantage.Adapter):
        self.adapter = adapter

    def get_quote_endpoint(self, symbol):
        '''Return Qoute object with current price, volume and stats of the symbol'''
        return self.adapter.get_quote_endpoint(symbol)
