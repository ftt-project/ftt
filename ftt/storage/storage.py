import pathlib
from typing import List

from peewee import Database

from ftt.storage.models.base import Base
from ftt.storage.storage_manager import StorageManager


class DatabaseNotInitialized(Exception):
    pass


class Storage:
    _instance = None

    def __init__(
        self, application_name: str, environment: str, root_path: pathlib.Path
    ):
        self._storage_manager: StorageManager = StorageManager(
            application_name, environment, root_path
        )
        self._initialized: bool = False

    def initialize(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self._storage_manager.initialize_database()

    def get_storage_manager(self) -> StorageManager:
        return self._storage_manager

    @classmethod
    def storage_manager(cls) -> StorageManager:
        if not cls._instance:
            raise DatabaseNotInitialized()

        return cls._instance.get_storage_manager()

    @staticmethod
    def get_models() -> List[Base]:
        return Base.__subclasses__()

    @classmethod
    def initialize_database(
        cls, application_name: str, environment: str, root_path: pathlib.Path
    ):
        instance = cls(application_name, environment, root_path)
        instance.initialize()
        cls._instance = instance

    @classmethod
    def get_database(cls) -> Database:
        return cls.storage_manager().database
