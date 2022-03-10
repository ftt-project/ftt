from ftt.brokers.ib.ib_brokerage_factory import IBBrokerageFactory  # noqa.


def build_brokerage_service(name: str, config):
    """
    This is a helper method that configures request brokerage service class and
    returns configured BrokerageService as a generic interface for communication with any brokerage system

    Parameters
    ----------
    name : str
        The name of the brokerage system
    config : object
        Configuration DTO for correction brokerage system configuration
    """
    from ftt.brokers.brokerage_factory_registry import BrokerageFactoryRegistry
    from ftt.brokers.brokerage_service import BrokerageService

    broker_service_creator = BrokerageFactoryRegistry.get(name)
    creator = broker_service_creator(config)

    brokerage_service = BrokerageService(creator.build())

    return brokerage_service
