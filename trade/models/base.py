from datetime import datetime

from peewee import Model, DateTimeField
from trade.models import DatabaseConnection


class Base(Model):
    updated_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = DatabaseConnection()
