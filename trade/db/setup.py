from playhouse.postgres_ext import PostgresqlExtDatabase

pg_db = PostgresqlExtDatabase('postgres', user='postgres', password='postgres',
                              host='db', port=5432, autorollback=True)


def database_connection():
    return pg_db

def establish_connection():
    pg_db.connect()

def create_tables(models):
    establish_connection()
    database_connection().create_tables(models)
