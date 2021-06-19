import pytest

from trade.storage import Storage
from trade.storage.storage_manager import StorageManager


class TestStorage:
    @pytest.fixture
    def subject(self):
        return Storage(application_name='fams', environment='test')

    def test_get_manager(self, subject):
        result = subject.get_manager()
        assert type(result) == StorageManager

    def test_tables(self, subject):
        result = subject.get_tables()
        assert type(result) == list

