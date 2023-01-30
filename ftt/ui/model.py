from typing import Any, Union

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt
from pydantic import ValidationError

model = None


def get_model():
    global model
    if model is None:
        model = ApplicationModel()
    return model


class ApplicationModel:
    def __init__(self):
        self._portfolio_version_id = None
        self._portfolio_id = None

    @property
    def portfolio_id(self):
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, value):
        self._portfolio_id = value

    @property
    def portfolio_version_id(self):
        return self._portfolio_version_id

    @portfolio_version_id.setter
    def portfolio_version_id(self, value):
        self._portfolio_version_id = value

    def __repr__(self):
        return f"ApplicationModel(portfolio_id={self.portfolio_id}, portfolio_version_id={self.portfolio_version_id})"

    def __str__(self):
        return self.__repr__()


class CollectionModel(QAbstractTableModel):
    class HeaderMapping:
        def __init__(self, headers):
            self._headers = headers

        def __getitem__(self, item: int) -> str:
            """
            Returns the numan readable header name for the given column index.
            """
            keys = list(self._headers.keys())
            return self._headers[keys[item]]

        def __len__(self):
            return len(self._headers)

        def keys(self) -> set:
            """
            Returns the keys for the model.
            """
            return set(self._headers.keys())

        def key(self, param: int) -> str:
            """
            Returns the key for the given column index.
            """
            return list(self._headers.keys())[param]

    def __init__(self, collection: list, headers: dict[str, str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._collection = collection
        self._headers = self.HeaderMapping(headers)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._collection)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._headers)

    def data(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self._collection):
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            record = self._collection[index.row()]
            return record.dict(include=self._headers.keys())[
                self._headers.key(index.column())
            ]

        return None

    def setData(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        value: Any,
        role: int = Qt.ItemDataRole.EditRole,
    ):
        if not index.isValid():
            return False

        if not 0 <= index.row() < len(self._collection):
            return False

        if role != Qt.ItemDataRole.EditRole:
            return False

        record = self._collection[index.row()]
        updated_record = record.copy(update={self._headers.key(index.column()): value})
        try:
            record.validate(updated_record.dict(by_alias=False, exclude_unset=True))
            self._collection[index.row()] = updated_record
        except ValidationError:
            return False

        return True

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal and section < len(self._headers):
            return self._headers[section]

        return None

    def add(self, item):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._collection.append(item)
        self.endInsertRows()

    def remove(self, index):
        if not index.isValid():
            return False

        self.beginRemoveRows(index, index.row(), index.row())
        self._collection.pop(index.row())
        self.endRemoveRows()

    def clear(self):
        self.beginResetModel()
        self._collection.clear()
        self.endResetModel()

    def __contains__(self, item):
        return item in self._collection

    def __getitem__(self, item):
        return self._collection[item]

    def __setitem__(self, key, value):
        self._collection[key] = value

    def __delitem__(self, key):
        self.remove(key)

    def __len__(self):
        return len(self._collection)

    def __repr__(self):
        return f"CollectionModel({self._collection})"

    def __str__(self):
        return self.__repr__()
