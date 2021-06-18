from abc import ABC, abstractmethod

from trade.storage.models import Base


class RepositoryInterface(ABC):
    @staticmethod
    @abstractmethod
    def create(self, data: dict) -> Base:
        pass

    @staticmethod
    @abstractmethod
    def save(self, model: Base) -> Base:
        pass

    @staticmethod
    @abstractmethod
    def get_by_id(self, id: int) -> Base:
        pass
