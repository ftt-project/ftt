import os

import pytest
from peewee import Database

from ftt.storage import Storage
from ftt.storage.storage_manager import StorageManager


class TestStorage:
    @pytest.fixture
    def subject(self):
        return Storage

    def test_get_manager(self, subject):
        result = subject.storage_manager()
        assert type(result) == StorageManager

    def test_tables(self, subject):
        result = subject.get_models()
        assert type(result) == list

    def test_get_database(self, subject):
        subject.initialize_database(
            application_name="ftt", environment="test", root_path=os.getcwd()
        )
        result = subject.get_database()
        assert isinstance(result, Database)
