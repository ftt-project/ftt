import pathlib
from typing import List, Optional

from peewee import Database

from ftt.storage.models.base import Base
from ftt.storage.storage_manager import StorageManager


class DatabaseNotInitialized(Exception):
    pass


class Storage:
    __storage_manager: Optional[StorageManager] = None

    @classmethod
    def storage_manager(cls) -> StorageManager:
        if not Storage.__storage_manager or not cls.__storage_manager.database:
            raise DatabaseNotInitialized()

        return cls.__storage_manager

    @staticmethod
    def get_models() -> List[Base]:
        return Base.__subclasses__()

    @classmethod
    def initialize_database(
        cls, application_name: str, environment: str, root_path: pathlib.Path
    ) -> None:
        if Storage.__storage_manager is not None:
            return

        storage_manager = StorageManager(application_name, environment, root_path)
        storage_manager.initialize_database()
        Storage.__storage_manager = storage_manager

    @classmethod
    def get_database(cls) -> Database:
        return cls.storage_manager().database
