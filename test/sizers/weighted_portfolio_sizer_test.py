import pytest
import pytest as pytest

from test import testcommon
import backtrader as bt
from datetime import datetime

from trade.db import Portfolio, Ticker, Weight
from trade.sizers.weighted_portfolio_sizer import WeightedPortfolioSizer


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

    def planned_position(self):
        return 10

    def current_position(self):
        return 2

    def ticker_name(self):
        return "SHOP"

    def setup(self):
        Weight.delete().execute()
        Ticker.delete().execute()
        Portfolio.delete().execute()

        self.ticker = Ticker.insert(
            ticker=self.ticker_name(),
            exchange="TOR",
            exchange_name="TOR",
            type="stock",
            type_display="stock",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ).execute()

        self.portfolio = Portfolio.insert(
            name="P1"
        ).execute()

        self.weight = Weight.insert(
            portfolio=self.portfolio,
            ticker=self.ticker,
            position=self.current_position(),
            planned_position=self.planned_position()
        ).execute()

    def prepare_cerebro(self, data=None):
        data = self.data() if data is None else data

        cerebro = bt.Cerebro()
        cerebro.addstrategy(self.strategy(), portfolio_id=self.portfolio)
        cerebro.addsizer(WeightedPortfolioSizer)
        cerebro.adddata(data, name=self.ticker_name())
        return cerebro

    def test_properly_utilized_by_cerebro(self):
        self.setup()
        cerebro = self.prepare_cerebro()
        strats = cerebro.run()

        strat = strats[0]
        assert type(strat.getsizer()) == WeightedPortfolioSizer

    def test_returns_on_buy_diff_from_portfolio(self):
        self.setup()
        cerebro = self.prepare_cerebro()
        strats = cerebro.run()

        strat = strats[0]
        sizer = strat.getsizer()
        result = sizer.getsizing(strat.data, True)
        assert 8 == result

    def test_returns_on_sell_0(self):
        assert False
