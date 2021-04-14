from peewee import Model
from trade.db import DatabaseConnection

class Base(Model):
    class Meta:
        database = DatabaseConnection()
