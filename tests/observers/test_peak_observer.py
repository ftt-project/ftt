from datetime import datetime
from decimal import Decimal

from trade.models import Order
from trade.observers.peak_observer import PeakObserver
import pytest
from tests import testcommon
from trade.repositories import WeightsRepository
from trade.strategies import BollingerStrategy
from trade.strategies.dummy_buy_once_strategy import DummyBuyOnceStrategy


class TestPeakObserver:
    @pytest.fixture
    def subject(self):
        return PeakObserver

    def test_stores_peak_value(self, subject, cerebro, weight):
        data = testcommon.getdata(1, fromdate=datetime(2020, 6, 1), todate=datetime(2020, 8, 30))
        c = cerebro([BollingerStrategy], data)
        c.addobserver(subject)
        result = c.run()
        assert Decimal("23.39") == WeightsRepository.get_by_id(weight.id).peaked_value
        Order.delete().execute()
