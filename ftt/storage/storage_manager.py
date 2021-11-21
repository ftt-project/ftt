from typing import List, Optional, ContextManager

from peewee import SqliteDatabase  # type: ignore

from ftt.storage.models.base import Base, database_proxy


class StorageManager:
    def __init__(self, db_name: str, environment: str, path: Optional[str] = None):
        self.db_name = db_name
        self.environment = environment
        self.database: ContextManager[SqliteDatabase] = None

    def initialize_database(self, adapter=SqliteDatabase) -> None:
        database = adapter(f"{self.db_name}.{self.environment}.db")
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
