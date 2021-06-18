from datetime import datetime
from decimal import Decimal

import pytest

from tests import testcommon
from trade.storage.models import Order
from trade.piloting.observers.peak_observer import PeakObserver
from trade.storage.repositories import OrdersRepository, WeightsRepository
from trade.piloting.strategies import ValueProtectingStrategy
from trade.piloting.strategies.dummy_buy_once_strategy import DummyBuyOnceStrategy


class TestValueProtectingStrategy:
    @pytest.fixture
    def subject(self):
        return ValueProtectingStrategy

    def test_runs(self, subject, cerebro, portfolio):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 11))

        orders_before = OrdersRepository().get_orders_by_portfolio(portfolio)
        c = cerebro([DummyBuyOnceStrategy, (subject, {"dipmult": 1.0})], data)
        c.addobserver(PeakObserver)
        broker = c.getbroker()
        c.run()
        orders_after = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert (len(orders_after) - len(orders_before)) == 2
        assert 29987.44 == broker.get_value()
        Order.delete().execute()

    def test_after_sell_weight_is_locked(self, subject, cerebro, weight):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2020, 5, 14, 23, 59, 59))
        c = cerebro([DummyBuyOnceStrategy, (subject, {"dipmult": 1.0})], data)
        c.addobserver(PeakObserver)
        c.run()
        weight = WeightsRepository.get_by_id(weight.id)
        assert weight.locked_at is not None
        assert weight.locked_at_amount == Decimal('14.10')
        Order.delete().execute()

    def test_after_buy_is_unlocked(self, subject, cerebro, weight):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 30))
        c = cerebro([DummyBuyOnceStrategy, subject], data)
        c.addobserver(PeakObserver)
        c.run()
        weight = WeightsRepository.get_by_id(weight.id)
        assert weight.locked_at is None
        assert weight.locked_at_amount is None
        Order.delete().execute()

    def test_buys_when_buy_enabled_is_true(self, subject, cerebro, portfolio, weight):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2020, 7, 1))
        orders_before = OrdersRepository().get_orders_by_portfolio(portfolio)
        c = cerebro([DummyBuyOnceStrategy, (subject, {"buy_enabled": True})], data)
        c.addobserver(PeakObserver)
        broker = c.getbroker()
        c.run()
        orders_after = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert (len(orders_after) - len(orders_before)) == 8
        assert 30019.040008 == broker.get_value()
        Order.delete().execute()