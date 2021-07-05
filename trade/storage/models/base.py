from datetime import datetime

from peewee import DatabaseProxy, DateTimeField, Model

database_proxy = DatabaseProxy()


class Base(Model):
    updated_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = database_proxy
