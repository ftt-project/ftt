import pytest
from PySide6.QtCore import Qt
from pydantic import BaseModel

from ftt.ui.model import CollectionModel


class TestCollectionModel:

    class ShowFlake(BaseModel):
        id: int
        name: str
        age: int
        type: str

    @pytest.fixture
    def collection(self):
        return [
            self.ShowFlake(id=1, name="foo", age=1, type="bar"),
            self.ShowFlake(id=2, name="baz", age=2, type="qux"),
            self.ShowFlake(id=3, name="quux", age=3, type="quuz"),
        ]

    @pytest.fixture
    def headers(self):
        return ["name", "age", "type"]

    @pytest.fixture
    def subject(self, collection, headers):
        return CollectionModel(
            collection=collection,
            headers=headers,
        )

    def test_row_count(self, subject):
        assert subject.rowCount() == 3

    def test_column_count(self, subject):
        assert subject.columnCount() == 3

    def test_data(self, subject):
        assert subject.data(subject.index(0, 0)) == "foo"
        assert subject.data(subject.index(0, 1)) == 1
        assert subject.data(subject.index(0, 2)) == "bar"

    def test_data_invalid_index(self, subject):
        assert subject.data(subject.index(3, 0)) is None
        assert subject.data(subject.index(0, 3)) is None

    def test_data_invalid_role(self, subject):
        assert subject.data(subject.index(0, 0), role=Qt.EditRole) is None

    def test_header_data(self, subject):
        assert subject.headerData(0, Qt.Horizontal) == "name"
        assert subject.headerData(1, Qt.Horizontal) == "age"
        assert subject.headerData(2, Qt.Horizontal) == "type"
        assert subject.headerData(3, Qt.Horizontal) is None

    def test_header_data_invalid_role(self, subject):
        assert subject.headerData(0, Qt.Horizontal, role=Qt.EditRole) is None

    def test_header_data_invalid_orientation(self, subject):
        assert subject.headerData(0, Qt.Vertical) is None

    def test_set_data(self, subject):
        assert subject.setData(subject.index(0, 0), "new value")
        assert subject.data(subject.index(0, 0)) == "new value"

    def test_set_data_invalid_index(self, subject):
        assert not subject.setData(subject.index(3, 0), "new value")
        assert not subject.setData(subject.index(0, 3), "new value")

    def test_set_data_invalid_role(self, subject):
        assert not subject.setData(subject.index(0, 0), "new value", role=Qt.DisplayRole)

    def test_set_data_invalid_value(self, subject):
        assert not subject.setData(subject.index(0, 0), [])

    def test_add_row(self, subject):
        assert subject.rowCount() == 3
        subject.add(self.ShowFlake(id=4, name="quux", age=3, type="quuz"))
        assert subject.rowCount() == 4

    def test_remove_row(self, subject):
        assert subject.rowCount() == 3
        subject.remove(subject.index(0, 0))
        assert subject.rowCount() == 2

    def test_remove_row_invalid_index(self, subject):
        assert subject.rowCount() == 3
        result = subject.remove(subject.index(3, 0))
        assert not result
        assert subject.rowCount() == 3

    def test_clear(self, subject):
        assert subject.rowCount() == 3
        subject.clear()
        assert subject.rowCount() == 0