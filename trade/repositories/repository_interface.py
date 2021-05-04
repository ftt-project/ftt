from abc import ABC, abstractmethod

from trade.models import Base


class RepositoryInterface(ABC):
    @abstractmethod
    def save(self, model: Base) -> Base:
        pass

    @abstractmethod
    def create(self, data: dict) -> Base:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Base:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Base:
        pass
