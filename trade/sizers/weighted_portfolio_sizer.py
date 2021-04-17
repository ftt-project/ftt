import backtrader as bt
import peewee

# https://community.backtrader.com/topic/144/feature-request-allow-passing-of-data-object-to-sizer
from trade.db import Portfolio, Ticker, Weight


class WeightedPortfolioSizer(bt.Sizer):
    params = (("dataname", None), ("portfolio_id", None))

    def _getsizing(self, comminfo, cash, data, isbuy):
        # portfolio = Portfolio.get_weights(self.p.dataname)
        weights = (Weight.select()
                   .join(Portfolio, peewee.JOIN.LEFT_OUTER)
                   .switch(Weight)
                   .join(Ticker, peewee.JOIN.LEFT_OUTER)
                   .where(Portfolio.id == self.p.portfolio_id)
                   .where(Ticker.ticker == self.p.dataname)
                   .get())
        self._data = self.strategy.getdatabyname(self.p.dataname)

        return weights.planned_position - weights.position
