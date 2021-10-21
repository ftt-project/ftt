from datetime import datetime
from decimal import Decimal

from ftt.storage.models.order import Order
from ftt.piloting.observers.peak_observer import PeakObserver
import pytest
from tests import testcommon
from ftt.storage.repositories.weights_repository import WeightsRepository
from ftt.piloting.strategies import BollingerStrategy


class TestPeakObserver:
    @pytest.fixture
    def subject(self):
        return PeakObserver

    def test_stores_peak_value(self, subject, cerebro, weight):
        data = testcommon.getdata(
            1, fromdate=datetime(2020, 6, 1), todate=datetime(2020, 8, 30)
        )
        c = cerebro([BollingerStrategy], data)
        c.addobserver(subject)
        result = c.run()
        assert (
            Decimal("23.389999") == WeightsRepository.get_by_id(weight.id).peaked_value
        )
        Order.delete().execute()
