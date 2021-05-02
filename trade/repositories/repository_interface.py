from abc import ABC, abstractmethod

from trade.models import Base


class RepositoryInterface(ABC):
    @abstractmethod
    def save(self, model: Base):
        pass

    def create(self, data: dict):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def get_by_name(self, name: str):
        pass
