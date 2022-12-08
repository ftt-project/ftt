from abc import ABC
from dataclasses import asdict
from datetime import datetime

import peewee
from playhouse.shortcuts import update_model_from_dict  # type: ignore

from ftt.storage.value_objects import ValueObjectInterface
from ftt.storage.errors import PersistingError
from ftt.storage.models.base import Base


class Repository(ABC):
    @classmethod
    def _create(cls, model_class, data) -> Base:
        """
        Generic method of creating a new record in the database.
        Creates a model based on a given class and data dictionary.

        Parameters:
        ----------
            model_class (Base): Model class
            data (dict): Data dictionary

        Raises:
        ------
            ValueError: If the model class is not a subclass of Base

        Returns:
        -------
            Base: Model instance

        Deprecated way of creating models.
        """
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()

        # TODO move protected method to base class
        fields = model_class.fields()
        difference = set(list(data.keys()) + ["id"]) - set(fields)
        if len(difference) > 0:
            raise ValueError(
                f"The following fields are not in the {model_class} definition: {difference}"
            )
        result = model_class.create(**data)
        return result

    @classmethod
    def _update(cls, instance, data: ValueObjectInterface) -> Base:
        try:
            dict_data = asdict(data)
            present_data = {k: v for k, v in dict_data.items() if v is not None}
            present_data["updated_at"] = datetime.now()
            model = update_model_from_dict(instance, present_data)
            model.save()
        except (AttributeError, peewee.IntegrityError) as e:
            raise PersistingError(instance, data, str(e))

        return model

    @classmethod
    def _delete(cls, instance, soft_delete: bool = True) -> bool:
        if soft_delete:
            instance.deleted_at = datetime.now()
            result = instance.save()
        else:
            result = instance.delete_instance()
        return result == 1

    @classmethod
    def _get_by_id(cls, model_class, id: int) -> Base:
        return model_class.get(id)
