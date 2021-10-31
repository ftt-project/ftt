from datetime import datetime
from typing import List

from peewee import DatabaseProxy, DateTimeField, Model

database_proxy = DatabaseProxy()


class Base(Model):
    updated_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = database_proxy

    @classmethod
    def fields(cls) -> List[str]:
        """
        Return a list of field names for the model for validation purposes.
        """
        return [f.column.name for f in cls._meta.sorted_fields]
