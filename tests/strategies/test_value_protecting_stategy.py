import pytest
import backtrader as bt
from backtrader import DataBase

from tests import testcommon
from trade.models import Order
from trade.repositories import OrdersRepository
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
        data = testcommon.getdata(0)

        orders_before = OrdersRepository().get_orders_by_portfolio(portfolio)
        c = cerebro([self.__class__.DummyBuyOnceStrategy, subject], data)
        broker = c.getbroker()
        c.run()
        orders_after = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert (len(orders_after) - len(orders_before)) == 2
        assert 29744.88 == broker.get_value()
        Order.delete().execute()
