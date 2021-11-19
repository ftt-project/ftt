from abc import ABC


class DTOInterface(ABC):
    pass


def is_empty(dto_object: DTOInterface) -> bool:
    return all([field is None for field in dto_object.__dict__.values()])
