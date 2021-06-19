from typing import Optional, List

from peewee import SqliteDatabase

from trade.storage.models import Base
from trade.storage.storage_manager import StorageManager


class Storage:
    database: Optional[SqliteDatabase] = None

    def __init__(self, application_name, environment):
        self.application_name = application_name
        self.environment = environment

    def get_manager(self) -> StorageManager:
        return StorageManager(self.application_name, self.environment)

    def get_tables(self) -> List[Base]:
        return Base.__subclasses__()