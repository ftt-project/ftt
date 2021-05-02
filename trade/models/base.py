from peewee import Model
from trade.models import DatabaseConnection


class Base(Model):
    class Meta:
        database = DatabaseConnection()
