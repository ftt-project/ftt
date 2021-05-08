import pytest
from test import testcommon
import backtrader as bt

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

    @pytest.mark.skip(reason="Broken")
    def prepare_cerebro(self, ticker_name, data=None):
        data = self.data() if data is None else data

        cerebro = bt.Cerebro()
        cerebro.addstrategy(self.strategy(), portfolio_id=self.portfolio)
        cerebro.addsizer(WeightedPortfolioSizer)
        cerebro.adddata(data, name=self.ticker_name())
        return cerebro

    @pytest.mark.skip(reason="Broken")
    def test_properly_utilized_by_cerebro(self, weights_seed):
        cerebro = self.prepare_cerebro(weights_seed.symbol.symbol)
        strats = cerebro.run()

        strat = strats[0]
        assert type(strat.getsizer()) == WeightedPortfolioSizer

    @pytest.mark.skip(reason="Broken")
    def test_returns_on_buy_diff_from_portfolio(self, weights_seed):
        cerebro = self.prepare_cerebro(weights_seed.symbol.symbol)
        strats = cerebro.run()

        strat = strats[0]
        sizer = strat.getsizer()
        result = sizer.getsizing(strat.data, True)
        assert 8 == result

    @pytest.mark.skip(reason="Not implemented")
    def test_returns_on_sell_0(self):
        assert False
