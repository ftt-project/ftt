from peewee import Model
from playhouse.postgres_ext import PostgresqlExtDatabase

pg_db = PostgresqlExtDatabase('trade', user='postgres', password='trade',
                              host='127.0.0.1', port=5432, register_hstore=True, autorollback=True)


class BaseModel(Model):
    class Meta:
        database = pg_db


def database_connection():
    return pg_db


def establish_connection():
    pg_db.connect()
