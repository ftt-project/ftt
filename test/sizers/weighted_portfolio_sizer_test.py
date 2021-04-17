from test import testcommon
import backtrader as bt
from datetime import datetime

from trade.db import Portfolio, Ticker, Weight
from trade.sizers.weighted_portfolio_sizer import WeightedPortfolioSizer


class TestWeightedPortfolioSizer:
    class DummyStrategy(bt.Strategy):
        def next(self):
            self.buy()

    def broker(self):
        return bt.brokers.BackBroker()

    def strategy(self):
        return TestWeightedPortfolioSizer.DummyStrategy

    def data(self, did=0):
        return testcommon.getdata(did)

    def prepare_portfolio(self):
        Weight.delete().execute()
        Ticker.delete().execute()
        Portfolio.delete().execute()

        self.ticker = Ticker.insert(
            ticker="SHOP",
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
            position=2,
            planned_position=10
        ).execute()

    def prepare_cerebro(self, data=None):
        data = self.data() if data is None else data

        cerebro = bt.Cerebro()
        cerebro.addstrategy(self.strategy())
        cerebro.addsizer(WeightedPortfolioSizer, dataname="SHOP", portfolio_id=self.portfolio)
        cerebro.adddata(data, name="SHOP")
        return cerebro

    def test_properly_utilized_by_cerebro(self):
        self.prepare_portfolio()
        cerebro = self.prepare_cerebro()
        strats = cerebro.run()

        strat = strats[0]
        assert type(strat.getsizer()) == WeightedPortfolioSizer

    def test_returns_on_buy_diff_from_portfolio(self):
        self.prepare_portfolio()
        cerebro = self.prepare_cerebro()
        strats = cerebro.run()


        sizer = strats[0].getsizer()
        result = sizer.getsizing(self.data(), True)
        assert 8 == result
