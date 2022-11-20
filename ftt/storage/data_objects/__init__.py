from abc import ABC


class ValueObjectInterface(ABC):
    pass


def is_empty(value_object: ValueObjectInterface) -> bool:
    return all([field is None for field in value_object.__dict__.values()])
