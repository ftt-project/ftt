from abc import ABC
from dataclasses import asdict
from datetime import datetime

import peewee
from playhouse.shortcuts import update_model_from_dict  # type: ignore

from ftt.storage.data_objects import DTOInterface
from ftt.storage.errors import PersistingError
from ftt.storage.models.base import Base


class Repository(ABC):
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

    @classmethod
    def _update(cls, instance, data: DTOInterface) -> Base:
        try:
            dict_data = asdict(data)
            present_data = {k: v for k, v in dict_data.items() if v is not None}
            present_data["updated_at"] = datetime.now()
            model = update_model_from_dict(instance, present_data)
            model.save()
        except (AttributeError, peewee.IntegrityError) as e:
            raise PersistingError(instance, data, str(e))

        return model
