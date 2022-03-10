import pytest

from ftt.brokers.brokerage_factory_registry import BrokerageFactoryRegistry
from ftt.brokers.ib.ib_brokerage_factory import IBBrokerageFactory


class TestBrokerageFactoryRegistry:
    @pytest.fixture
    def subject(self):
        return BrokerageFactoryRegistry

    def test_registers_existing_factories(self, subject):
        assert subject.get_registry() == {"Interactive Brokers": IBBrokerageFactory}

    def test_returns_factory_by_provider_name(self, subject):
        result = subject.get("Interactive Brokers")
        assert result == IBBrokerageFactory
        assert result.provider_name == "Interactive Brokers"
