class BrokerageFactoryRegistry(type):
    """
    Metaclass that register each concrete Brokerage Service implementation
    """

    REGISTRY: dict[str, type] = {}

    def __new__(mcs, name, bases, attrs):
        new_cls = type.__new__(mcs, name, bases, attrs)
        if not new_cls.__name__ == "BaseBrokerageFactory":
            mcs.REGISTRY[new_cls.provider_name] = new_cls

        return new_cls

    @classmethod
    def get_registry(mcs):
        return dict(mcs.REGISTRY)

    @classmethod
    def get(mcs, brokerage_provider):
        registry = mcs.get_registry()
        return registry.get(brokerage_provider)
