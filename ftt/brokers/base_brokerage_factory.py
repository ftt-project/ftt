from ftt.brokers.brokerage_factory_registry import BrokerageFactoryRegistry


class BaseBrokerageFactory(metaclass=BrokerageFactoryRegistry):
    """
    A base class that each brokerage factory must inherit.
    """

    @property
    def provider_name(self, *args, **kwargs):
        """
        This method must be inherited by concrete factory.
        Returns name of the provider that a factory builds.
        """
        raise NotImplementedError

    def build(self):
        """
        Must be implemented in concreteBrokerageService factory class
        """
        raise NotImplementedError
