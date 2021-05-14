from datetime import datetime

import pytest
import backtrader as bt

from tests import testcommon
from trade.models import Order, Ticker
from trade.repositories import OrdersRepository
from trade.strategies.sizers import WeightedSizer
from trade.strategies.sma_crossover_strategy import SMACrossoverStrategy


class TestSMACrossoverStrategy:
    @pytest.fixture
    def subject(self):
        return SMACrossoverStrategy

    @pytest.fixture
    def cerebro(self, subject, portfolio_version, ticker, weight):
        def _cerebro(data):
            cerebro = bt.Cerebro(live=True, cheat_on_open=True)
            cerebro.addstrategy(subject, portfolio_version_id=portfolio_version.id)
            cerebro.addsizer(WeightedSizer)

            cerebro.adddata(data, name=ticker.symbol)

            cerebro.broker.setcash(30000.0)
            return cerebro

        return _cerebro

    def test_buys_with_given_cash_allocation_and_one_ticker(self, subject, cerebro):
        data = testcommon.getdata(3, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 13))
        c = cerebro(data)
        result = c.run()
        assert 29018.365783691406 == c.broker.cash
        assert 30000.92578125 == c.broker.getvalue()
        assert type(result[0]) == subject
        assert type(result[0]._orders) == list
        Order.delete().execute()

    def test_orders_against_data0(self, cerebro, portfolio):
        data = testcommon.getdata(3, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 13))
        orders_before = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert len(orders_before) == 0
        _ = cerebro(data).run()
        orders_after = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert len(orders_after) == 2
        Order.delete().execute()

