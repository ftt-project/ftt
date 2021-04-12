from peewee import Model
from trade.db.setup import database_connection

def create_tables():
    models = Base.__subclasses__()
    database_connection().create_tables(models)

class Base(Model):
    class Meta:
        database = database_connection()