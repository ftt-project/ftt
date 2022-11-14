from datetime import datetime
from typing import List

from peewee import DatabaseProxy, DateTimeField, Model

database_proxy = DatabaseProxy()


class Base(Model):
    updated_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now)
    deleted_at = DateTimeField(null=True)

    class Meta:
        database = database_proxy

    @classmethod
    def fields(cls) -> List[str]:
        """
        Return a list of field names for the model for validation purposes.
        """
        return [f.column.name for f in cls._meta.sorted_fields]

    @classmethod
    def select(cls, *fields):
        return super().select(*fields).where(cls.deleted_at.is_null())

    @classmethod
    def select_all(cls, *fields):
        return super().select(*fields)

    @classmethod
    def select_deleted(cls, *fields):
        return super().select(*fields).where(cls.deleted_at.is_null(False))
