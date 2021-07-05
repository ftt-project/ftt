import pytest
from trade.storage.storage_manager import StorageManager
from trade.storage.models.security import Security


class TestStorageManager:
    @pytest.fixture
    def subject(self):
        return StorageManager(db_name='ftt', environment='test')

    @pytest.fixture
    def context(self, mocker):
        db = mocker.Mock()
        db.__enter__ = db
        db.__exit__ = db
        return db

    @pytest.mark.skip(reason="Interfere with tests out of the scope: TypeError: object of type 'Mock' has no len()")
    def test_initialize_database(self, subject, mocker):
        stub = mocker.stub(name='SqliteDatabase')
        subject.initialize_database(stub)
        stub.assert_called_once_with(f"ftt.test.db")

    @pytest.mark.skip(reason="Interfere with tests out of the scope: TypeError: object of type 'Mock' has no len()")
    def test_run_migrations(self, subject, mocker, context):
        mock = mocker.Mock()
        mock.return_value = context

        subject.initialize_database(mock)
        subject.create_tables([Security])
        context.assert_has_calls([mocker.call(), mocker.call.create_tables([Security]), mocker.call(None, None, None)])

    def test_drop_tables(self, subject, mocker):
        model = mocker.Mock()

        subject.drop_tables([model])
        model.drop_table.assert_called_once()

