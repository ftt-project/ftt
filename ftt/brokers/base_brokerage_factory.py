from ftt.brokers.brokerage_factory_registry import BrokerageFactoryRegistry


class BaseBrokerageFactory(metaclass=BrokerageFactoryRegistry):
    """
    A base class that each brokerage factory must inherit.
    """

    def build(self):
        """
        Must be implemented in concreteBrokerageService factory class
        """
        raise NotImplementedError
