import os
from dotenv import load_dotenv
from peewee import DatabaseProxy, OperationalError
from playhouse.postgres_ext import PostgresqlExtDatabase

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv(dotenv_path=os.environ["ENV_FILE"])

config = {
    "database": os.environ['DB_NAME'],
    "user": os.environ['DB_USER'],
    "password": os.environ['DB_PASSWORD'],
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
}

database = PostgresqlExtDatabase(config["database"], user=config["user"], password=config["password"],
                                 host=config["host"], port=config["port"], autorollback=True)


database_proxy = DatabaseProxy()
database_proxy.initialize(database)


def database_connection():
    return database


def establish_connection():
    connection = database_connection()
    connection.connect()


def create_database():
    conn = psycopg2.connect(host=config["host"], database="postgres", user=config["user"],
                            password=config["password"])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
    conn.cursor().execute(f"CREATE DATABASE {config['database']} WITH OWNER {config['user']}")
    conn.close()


def create_tables(models):
    establish_connection()
    connection = database_connection()
    connection.create_tables(models)
