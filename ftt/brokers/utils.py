from ftt.brokers.ib.ib_brokerage_factory import IBBrokerageFactory  # noqa.


_brokerage_service = None


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

    global _brokerage_service

    if _brokerage_service is not None:
        return _brokerage_service

    broker_service_creator = BrokerageFactoryRegistry.get(name)
    creator = broker_service_creator(config)

    _brokerage_service = creator.build()

    brokerage_service = BrokerageService(_brokerage_service)

    return brokerage_service
