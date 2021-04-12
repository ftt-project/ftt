from peewee import Model
from trade.db.setup import pg_db


class Base(Model):
    class Meta:
        database = pg_db