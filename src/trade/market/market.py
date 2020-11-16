from src.trade.market.adapters import yfinance
from src.trade.market.adapters import alpha_vantage


class Market(object):
    def __init__(self, adapter=yfinance.Adapter):
        self.adapter = adapter

    def get_quote(self, qoute):
        """Return Quote object with current price, volume and stats of the symbol"""
        return self.adapter.get_quote(qoute.symbol)

    def get_quotes(self, quotes):
        symbols = [quote.symbol for quote in quotes]
        return self.adapter.get_quotes(symbols)
