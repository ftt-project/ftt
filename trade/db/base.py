from peewee import Model
from trade.db.setup import database_connection

class Base(Model):
    class Meta:
        database = database_connection()