from datetime import datetime

import pytest
import backtrader as bt
from tests import testcommon
from trade.models import Order
from trade.strategies.bollinger_strategy import BollingerStrategy


class TestBollingerStrategy:
    @pytest.fixture
    def subject(self):
        return BollingerStrategy

    def test_buys_with_given_cash_allocation_and_one_ticker(self, subject, cerebro):
        data = testcommon.getdata(3, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 13))
        c = cerebro([subject], data)
        result = c.run()
        assert 29013.119995117188 == c.broker.cash
        assert 29995.67999267578 == c.broker.getvalue()
        assert type(result[0]) == subject
        assert type(result[0]._orders) == list
        Order.delete().execute()
