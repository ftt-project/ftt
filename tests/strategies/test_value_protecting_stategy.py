from datetime import datetime
from decimal import Decimal

import pytest
import backtrader as bt
from backtrader import DataBase

from tests import testcommon
from trade.models import Order
from trade.repositories import OrdersRepository, WeightsRepository
from trade.strategies import ValueProtectingStrategy
from trade.strategies.base_strategy import BaseStrategy


class TestValueProtectingStrategy:
    class DummyBuyOnceStrategy(BaseStrategy):
        params = (
            ("portfolio_version_id", None),
        )

        def __init__(self):
            self.bought = False

        def buy_signal(self, data):
            if not self.bought:
                self.bought = True
                return True

            return False

        def sell_signal(self, data: DataBase):
            return False

    @pytest.fixture
    def subject(self):
        return ValueProtectingStrategy

    def test_runs(self, subject, cerebro, portfolio):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 11))

        orders_before = OrdersRepository().get_orders_by_portfolio(portfolio)
        c = cerebro([self.__class__.DummyBuyOnceStrategy, subject], data)
        broker = c.getbroker()
        c.run()
        orders_after = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert (len(orders_after) - len(orders_before)) == 2
        assert 29987.44 == broker.get_value()
        Order.delete().execute()

    def test_after_sell_weight_is_locked(self, subject, cerebro, weight):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2020, 5, 14, 23, 59, 59))
        c = cerebro([self.__class__.DummyBuyOnceStrategy, subject], data)
        c.run()
        weight = WeightsRepository.get_by_id(weight.id)
        assert weight.locked_at is not None
        assert weight.locked_at_amount == Decimal('14.10')
        Order.delete().execute()

    def test_after_buy_is_unlocked(self, subject, cerebro, weight):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 30))
        c = cerebro([self.__class__.DummyBuyOnceStrategy, subject], data)
        c.run()
        weight = WeightsRepository.get_by_id(weight.id)
        assert weight.locked_at is None
        assert weight.locked_at_amount is None
        Order.delete().execute()
