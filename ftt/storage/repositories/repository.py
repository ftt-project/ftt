from abc import ABC, abstractmethod
from datetime import datetime

from ftt.storage.models.base import Base


class Repository(ABC):
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

    @classmethod
    def _create(cls, model_class, data) -> Base:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()

        # TODO move protected method to base class
        fields = model_class.fields()
        difference = set(list(data.keys()) + ["id"]) - set(fields)
        # difference = set(fields).symmetric_difference(set(list(data.keys()) + ["id"]))
        if len(difference) > 0:
            raise ValueError(
                f"The following fields are not in the {model_class} definition: {difference}"
            )
        result = model_class.create(**data)
        return result
