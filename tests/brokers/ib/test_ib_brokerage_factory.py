import pytest

from ftt.brokers.brokerage_service import BrokerageService
from ftt.brokers.ib.ib_brokerage_factory import IBBrokerageFactory
from ftt.brokers.ib.ib_brokerage_service import IBBrokerageService


class TestIBBrokerageFactory:
    @pytest.fixture
    def subject(self):
        return IBBrokerageFactory

    def test_returns_configured_ib_brokerage_service(self, subject, config):
        factory = subject(config)
        result = factory.build()

        assert type(result) == BrokerageService
        assert result.provider_name == IBBrokerageService.provider_name
