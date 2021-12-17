import os

import peewee
# import psycopg2  # type: ignore
from dotenv import dotenv_values
# from playhouse.postgres_ext import PostgresqlExtDatabase  # type: ignore
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # type: ignore

from ftt.logger import logger


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
    # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.cursor().execute(
        f"CREATE DATABASE {config['database']} WITH OWNER {config['user']}"
    )
    conn.close()


def create_tables(models) -> None:
    try:
        establish_connection()
    except peewee.OperationalError as e:
        logger.error(f"{e}")

    connection = database_connection()
    connection.create_tables(models)
    logger.info(f"Tables {models} were created")


def drop_tables(models) -> None:
    try:
        establish_connection()
    except peewee.OperationalError as e:
        logger.error(f"{e}")

    connection = database_connection()
    connection.drop_tables(models)
    logger.info(f"Tables {models} were dropped")
