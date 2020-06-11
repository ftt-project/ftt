from src.trade.market.adapters import yfinance


class Market(object):
    def __init__(self, adapter=yfinance.Adapter):
        self.adapter = adapter

    def get_quote(self, qoute):
        """Return Quote object with current price, volume and stats of the symbol"""
        return self.adapter.get_quote(qoute.symbol)
