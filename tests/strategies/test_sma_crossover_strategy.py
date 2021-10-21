from datetime import datetime

import pytest

from tests import testcommon
from ftt.storage.models.order import Order
from ftt.storage.repositories.orders_repository import OrdersRepository
from ftt.piloting.strategies.sma_crossover_strategy import SMACrossoverStrategy


class TestSMACrossoverStrategy:
    @pytest.fixture
    def subject(self):
        return SMACrossoverStrategy

    def test_buys_with_given_cash_allocation_and_one_ticker(self, subject, cerebro):
        data = testcommon.getdata(
            3, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 13)
        )
        c = cerebro([subject], data)
        result = c.run()
        assert 29018.365783691406 == c.broker.cash
        assert 30000.92578125 == c.broker.getvalue()
        assert type(result[0]) == subject
        assert type(result[0]._orders) == list
        Order.delete().execute()

    def test_orders_against_data0(self, subject, cerebro, portfolio):
        data = testcommon.getdata(
            3, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 13)
        )
        orders_before = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert len(orders_before) == 0
        _ = cerebro([subject], data).run()
        orders_after = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert (len(orders_after) - len(orders_before)) == 19
        Order.delete().execute()
