import backtrader as bt
import peewee

# https://community.backtrader.com/topic/144/feature-request-allow-passing-of-data-object-to-sizer
from trade.db import Portfolio, Ticker, Weight


class WeightedPortfolioSizer(bt.Sizer):
    """
    TODO: Rename to WeightedSizer
    """
    params = (("dataname", None), ("portfolio_id", None))

    def _getsizing(self, comminfo, cash, data, isbuy):
        # portfolio = Portfolio.get_weights(self.p.dataname)
        # TODO: move this to Portfolio(Weight) class or service
        # TODO: handle sell event
        ticker_name = data._name
        portfolio_id = self.strategy.params.portfolio_id

        weights = (Weight.select()
                   .join(Portfolio, peewee.JOIN.LEFT_OUTER)
                   .switch(Weight)
                   .join(Ticker, peewee.JOIN.LEFT_OUTER)
                   .where(Portfolio.id == portfolio_id)
                   .where(Ticker.name == ticker_name)
                   .get())
        self._data = self.strategy.getdatabyname(ticker_name)

        return weights.planned_position - weights.position
