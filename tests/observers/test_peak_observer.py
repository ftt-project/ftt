from datetime import datetime
from decimal import Decimal

from trade.storage.models import Order
from trade.piloting.observers.peak_observer import PeakObserver
import pytest
from tests import testcommon
from trade.storage.repositories import WeightsRepository
from trade.piloting.strategies import BollingerStrategy


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
