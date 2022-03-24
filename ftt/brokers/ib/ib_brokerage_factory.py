from ftt.brokers.base_brokerage_factory import BaseBrokerageFactory
from ftt.brokers.ib.ib_brokerage_service import IBBrokerageService


class IBBrokerageFactory(BaseBrokerageFactory):
    """
    Factory class that creates and configures instance of IBBrokerageService.
    This class is added to BrokerageFactoryRegistry and must be not used directly.
    """

    provider_name: str = IBBrokerageService.provider_name

    def __init__(self, config):
        self._config = config

    def build(self):
        ib_broker = IBBrokerageService(
            self._config.host, self._config.port, self._config.client_id
        )
        return ib_broker
