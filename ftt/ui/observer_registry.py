from typing import Dict
from ftt.ui.observers.observer import Observer


class ObserverRegistry:

    REGISTRY: Dict[str, Observer] = {}

    @classmethod
    def register(cls, instance: Observer):
        cls.REGISTRY[instance.__class__.__name__] = instance

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)

    @classmethod
    def get_observer(cls, name):
        return cls.REGISTRY[name]
