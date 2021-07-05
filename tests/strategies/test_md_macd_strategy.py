from collections import Counter
from datetime import datetime

import pytest
from tests import testcommon
from trade.storage.models.order import Order
from trade.storage.repositories.orders_repository import OrdersRepository
from trade.piloting.strategies.md_macd_strategy import MdMACDStrategy


class TestMdMACDStrategy:
    """
    Implementation:
    - [ ] It must buy according to the given weights using Weight sizer
    """

    @pytest.fixture
    def subject(self):
        return MdMACDStrategy

    def test_buys_with_given_cash_allocation_and_one_ticker(self, subject, cerebro):
        data = testcommon.getdata(0)
        c = cerebro([subject], data)
        result = c.run()
        assert 28365.76 == c.broker.cash
        assert type(result[0]) == subject
        assert type(result[0]._orders) == list
        Order.delete().execute()

    @pytest.mark.skip(reason="Not implemented")
    def test_uses_the_total_cash_value(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_set_the_final_cash_value(self):
        pass

    def test_orders_against_data0(self, subject, cerebro, portfolio):
        data = testcommon.getdata(0)
        orders_before = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert len(orders_before) == 0
        _ = cerebro([subject], data).run()
        orders_after = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert len(orders_after) == 5
        Order.delete().execute()

    def test_orders_against_data1(self, subject, cerebro, portfolio):
        data = testcommon.getdata(1, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 11))

        orders_before = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert len(orders_before) == 0
        results = cerebro([subject], data).run()
        orders_after = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert len(orders_after) == 9
        types = Counter([o.type for o in orders_after])
        assert types["buy"] == 5
        assert types["sell"] == 4

        strat = results[0]
        assert strat.getposition().size == 8
        assert strat.getposition().price == 25.870001

        Order.delete().execute()

    @pytest.mark.skip(reason="Not implemented")
    def test_updates_position_value_in_weights(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_buys_positions(self):
        pass
