import os
import pathlib
from typing import List, ContextManager

from peewee import SqliteDatabase  # type: ignore

from ftt.storage.models.base import Base, database_proxy


class StorageManager:
    def __init__(self, db_name: str, environment: str, root_path: pathlib.Path):
        self.db_name = db_name
        self.environment = environment
        self.database: ContextManager[SqliteDatabase] = None
        self.root_path = root_path

    def initialize_database(self, adapter=SqliteDatabase) -> None:
        database = adapter(
            self.database_path(self.root_path, self.db_name, self.environment)
        )
        database_proxy.initialize(database)
        self.database = database

    def create_tables(self, tables: List[Base]) -> None:
        with self.database:
            self.database.create_tables(tables)

    def check_and_run_migration(self):
        raise NotImplementedError

    def drop(self):
        raise NotImplementedError

    def drop_tables(self, tables: List[Base]) -> None:
        for table in tables:
            table.drop_table()

    def seed_data(self):
        raise NotImplementedError

    @staticmethod
    def database_path(root_path, db_name, environment) -> str:
        return os.path.join(root_path, pathlib.Path(f"{db_name}.{environment}.db"))
