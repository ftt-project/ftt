import os
import pathlib
from types import TracebackType
from typing import List, Optional, Protocol, Type

from playhouse.sqliteq import SqliteQueueDatabase

from ftt.storage.models.base import Base, database_proxy


class DataBaseProtocol(Protocol):
    def __enter__(self):
        ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        ...

    def create_tables(self, list) -> None:
        ...


class StorageManager:
    def __init__(self, db_name: str, environment: str, root_path: pathlib.Path):
        self.db_name = db_name
        self.environment = environment
        self.database: Optional[DataBaseProtocol] = None
        self.root_path = root_path

    def initialize_database(self, adapter=SqliteQueueDatabase):
        database = adapter(
            self.database_path(self.root_path, self.db_name, self.environment),
            use_gevent=False,
            autostart=False,
            queue_max_size=64,  # Max. # of pending writes that can accumulate.
            results_timeout=5.0,  # Max. time to wait for query to be executed.
        )
        database.start()
        database_proxy.initialize(database)
        self.database = database

    def create_tables(self, tables: List[Base]) -> None:
        if not self.database:
            raise RuntimeError("Database not initialized")

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
