from ftt.brokers.brokerage_service import BrokerageService
from ftt.brokers.utils import build_brokerage_service


def test_build_brokerage_service(config):
    result = build_brokerage_service("Interactive Brokers", config)

    assert type(result) == BrokerageService
    assert result.provider_name == "Interactive Brokers"
