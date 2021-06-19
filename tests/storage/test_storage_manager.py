import pytest
from peewee import SqliteDatabase
from trade.storage.storage_manager import StorageManager
from trade.storage.models import Ticker


class TestStorageManager:
    @pytest.fixture
    def subject(self):
        return StorageManager(db_name='fams', environment='test')

    @pytest.fixture
    def context(self, mocker):
        db = mocker.Mock()
        db.__enter__ = db
        db.__exit__ = db
        return db

    def test_initialize_database(self, subject, mocker):
        stub = mocker.stub(name='SqliteDatabase')
        subject.initialize_database(stub)
        stub.assert_called_once_with(f"fams.test.db")

    def test_run_migrations(self, subject, mocker, context):
        mock = mocker.Mock()
        mock.return_value = context

        subject.initialize_database(mock)
        subject.create_tables([Ticker])
        context.assert_has_calls([mocker.call(), mocker.call.create_tables([Ticker]), mocker.call(None, None, None)])
