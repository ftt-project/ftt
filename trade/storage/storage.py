from typing import List

from peewee import Database

from trade.storage.models.base import Base
from trade.storage.storage_manager import StorageManager


class DatabaseNotInitialized(Exception):
    pass


class Storage:
    __storage_manager: StorageManager = None

    @classmethod
    def storage_manager(cls) -> StorageManager:
        if not Storage.__storage_manager or not cls.__storage_manager.database:
            raise DatabaseNotInitialized()

        return cls.__storage_manager

    @staticmethod
    def get_models() -> List[Base]:
        return Base.__subclasses__()

    @classmethod
    def initialize_database(cls, application_name, environment) -> None:
        if Storage.__storage_manager is not None:
            return

        storage_manager = StorageManager(application_name, environment)
        storage_manager.initialize_database()
        Storage.__storage_manager = storage_manager

    @classmethod
    def get_database(cls) -> Database:
        return cls.storage_manager().database
