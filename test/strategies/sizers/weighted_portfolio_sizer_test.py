from test import testcommon
import backtrader as bt
from datetime import datetime

from test.test_helper import weights_seed
from trade.db import Portfolio, Ticker, Weight
from trade.strategies.sizers import WeightedPortfolioSizer


class TestWeightedPortfolioSizer:
    class DummyStrategy(bt.Strategy):
        params = (("portfolio_id", None),)

        def next(self):
            for i, d in enumerate(self.datas):
                dt, dn = self.datetime.date(), d._name
                # position = self.getposition(d).size
                size = self.getsizing(d, True)
                self.buy()

    def strategy(self):
        return TestWeightedPortfolioSizer.DummyStrategy

    def data(self, did=0):
        return testcommon.getdata(did)

    def prepare_cerebro(self, ticker_name, data=None):
        data = self.data() if data is None else data

        cerebro = bt.Cerebro()
        cerebro.addstrategy(self.strategy(), portfolio_id=self.portfolio)
        cerebro.addsizer(WeightedPortfolioSizer)
        cerebro.adddata(data, name=self.ticker_name())
        return cerebro

    def test_properly_utilized_by_cerebro(self, weights_seed):
        cerebro = self.prepare_cerebro(weights_seed.ticker.ticker)
        strats = cerebro.run()

        strat = strats[0]
        assert type(strat.getsizer()) == WeightedPortfolioSizer

    def test_returns_on_buy_diff_from_portfolio(self, weights_seed):
        cerebro = self.prepare_cerebro(weights_seed.ticker.ticker)
        strats = cerebro.run()

        strat = strats[0]
        sizer = strat.getsizer()
        result = sizer.getsizing(strat.data, True)
        assert 8 == result

    def test_returns_on_sell_0(self):
        assert False
