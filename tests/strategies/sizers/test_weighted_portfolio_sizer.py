import pytest
from tests import testcommon
import backtrader as bt

from trade.strategies.sizers import WeightedPortfolioSizer


class TestWeightedPortfolioSizer:
    class DummyStrategy(bt.Strategy):
        params = (("portfolio_version_id", None),)

        def next(self):
            for i, d in enumerate(self.datas):
                dt, dn = self.datetime.date(), d._name
                # position = self.getposition(d).size
                size = self.getsizing(d, True)
                self.buy()

    @pytest.fixture
    def strategy(self):
        return TestWeightedPortfolioSizer.DummyStrategy

    @pytest.fixture
    def data(self, did=0):
        return testcommon.getdata(did)

    @pytest.fixture
    def cerebro(self, strategy, data, portfolio_version, ticker, weight):
        cerebro = bt.Cerebro()
        cerebro.addstrategy(strategy, portfolio_version_id=portfolio_version.id)
        cerebro.addsizer(WeightedPortfolioSizer)
        cerebro.adddata(data, name=ticker.symbol)
        return cerebro

    def test_properly_utilized_by_cerebro(self, cerebro):
        strats = cerebro.run()
        strat = strats[0]
        assert type(strat.getsizer()) == WeightedPortfolioSizer

    def test_returns_on_buy_diff_from_portfolio(self, cerebro):
        strats = cerebro.run()
        strat = strats[0]
        sizer = strat.getsizer()
        result = sizer.getsizing(strat.data, True)
        assert 8 == result

    @pytest.mark.skip(reason="Not implemented")
    def test_returns_on_sell_0(self):
        assert False
