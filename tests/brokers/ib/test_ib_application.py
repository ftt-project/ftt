import pytest

from ftt.brokers.ib.ib_brokerage_service import IBBrokerageService


class TestIBBrokerageService:
    @pytest.fixture
    def subject(self):
        return IBBrokerageService
