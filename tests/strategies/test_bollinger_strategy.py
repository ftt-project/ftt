from datetime import datetime

import pytest
from tests import testcommon
from trade.storage.models.order import Order
from trade.piloting.strategies import BollingerStrategy


class TestBollingerStrategy:
    @pytest.fixture
    def subject(self):
        return BollingerStrategy

    def test_buys_with_given_cash_allocation_and_one_ticker(self, subject, cerebro):
        data = testcommon.getdata(3, fromdate=datetime(2020, 5, 12), todate=datetime(2021, 5, 13))
        c = cerebro([subject], data)
        result = c.run()
        assert 29999.826416015625 == c.broker.cash
        assert 29999.826416015625 == c.broker.getvalue()
        assert type(result[0]) == subject
        assert type(result[0]._orders) == list
        Order.delete().execute()
