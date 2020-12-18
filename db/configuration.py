from peewee import Model, PostgresqlDatabase

pg_db = PostgresqlDatabase('trade', user='postgres', password='trade',
                           host='127.0.0.1', port=5432)


class BaseModel(Model):
    class Meta:
        database = pg_db


def database_connection():
    return pg_db


def establish_connection():
    pg_db.connect()
