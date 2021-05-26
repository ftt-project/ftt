from datetime import datetime
from decimal import Decimal

import pytest
import backtrader as bt
from backtrader import DataBase

from tests import testcommon
from trade.models import Order
from trade.repositories import OrdersRepository, WeightsRepository
from trade.strategies import ValueProtectingStrategy
from trade.strategies.dummy_buy_once_strategy import DummyBuyOnceStrategy


class TestValueProtectingStrategy:
    @pytest.fixture
    def subject(self):
        return ValueProtectingStrategy

    def test_runs(self, subject, cerebro, portfolio):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 11))

        orders_before = OrdersRepository().get_orders_by_portfolio(portfolio)
        c = cerebro([DummyBuyOnceStrategy, subject], data)
        broker = c.getbroker()
        c.run()
        orders_after = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert (len(orders_after) - len(orders_before)) == 2
        assert 29987.44 == broker.get_value()
        Order.delete().execute()

    def test_after_sell_weight_is_locked(self, subject, cerebro, weight):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2020, 5, 14, 23, 59, 59))
        c = cerebro([DummyBuyOnceStrategy, subject], data)
        c.run()
        weight = WeightsRepository.get_by_id(weight.id)
        assert weight.locked_at is not None
        assert weight.locked_at_amount == Decimal('14.10')
        Order.delete().execute()

    def test_after_buy_is_unlocked(self, subject, cerebro, weight):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 30))
        c = cerebro([DummyBuyOnceStrategy, subject], data)
        c.run()
        weight = WeightsRepository.get_by_id(weight.id)
        assert weight.locked_at is None
        assert weight.locked_at_amount is None
        Order.delete().execute()

    def test_buys_when_buy_enabled_is_true(self, subject, cerebro, portfolio, weight):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2020, 7, 1))
        orders_before = OrdersRepository().get_orders_by_portfolio(portfolio)
        c = cerebro([DummyBuyOnceStrategy, (subject, {"buy_enabled": True})], data)
        broker = c.getbroker()
        c.run()
        orders_after = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert (len(orders_after) - len(orders_before)) == 7
        assert 29990.640016 == broker.get_value()
        Order.delete().execute()