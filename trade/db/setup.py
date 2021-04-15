import os
from dotenv import dotenv_values
from peewee import DatabaseProxy, OperationalError
from playhouse.postgres_ext import PostgresqlExtDatabase

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def read_configuration():
    variables = dotenv_values(os.environ["ENV_FILE"])
    return {
        "database": variables["DB_NAME"],
        "user": variables["DB_USER"],
        "password": variables["DB_PASSWORD"],
        "host": variables["DB_HOST"],
        "port": variables["DB_PORT"],
    }


class DatabaseConnection:
    _instance = None

    def __new__(cls, config=read_configuration()):
        if cls._instance is None:
            cls._instance = PostgresqlExtDatabase(
                config["database"],
                user=config["user"],
                password=config["password"],
                host=config["host"],
                port=config["port"],
                autorollback=True,
            )
        return cls._instance


# database = PostgresqlExtDatabase(CONFIG["database"], user=CONFIG["user"], password=CONFIG["password"],
#                                  host=CONFIG["host"], port=CONFIG["port"], autorollback=True)
#
# database_proxy = DatabaseProxy()
# database_proxy.initialize(database)


def database_connection(config=read_configuration()):
    """
    TODO: remove function and singleton class
    """
    return DatabaseConnection(config)


def establish_connection():
    connection = database_connection()
    connection.connect()


def create_database():
    config = read_configuration()
    conn = psycopg2.connect(
        host=config["host"],
        database="postgres",
        user=config["user"],
        password=config["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.cursor().execute(
        f"CREATE DATABASE {config['database']} WITH OWNER {config['user']}"
    )
    conn.close()


def create_tables(models):
    establish_connection()
    connection = database_connection()
    connection.create_tables(models)
