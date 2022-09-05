from typing import Dict

from PySide6.QtCore import QAbstractListModel, Signal, Qt, QByteArray, QModelIndex
from result import Err, Ok

from ftt.handlers.portfolio_load_handler import PortfolioLoadHandler
from ftt.handlers.portfolio_versions_list_handler import PortfolioVersionsListHandler


class PortfolioModel(QAbstractListModel):
    IdentifierRole = Qt.UserRole + 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._portfolio_versions = []

    def roleNames(self) -> Dict[int, QByteArray]:
        roles = {
            self.__class__.IdentifierRole: QByteArray(b'identifier'),
            Qt.DisplayRole: QByteArray(b'display')
        }
        return roles

    def rowCount(self, index):
        return len(self._portfolio_versions)

    def data(self, index, role):
        d = self._portfolio_versions[index.row()]

        if role == Qt.DisplayRole:
            return d.optimization_strategy_name
        elif role == self.__class__.IdentifierRole:
            return d.id

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == self.__class__.IdentifierRole:
            self._portfolio_versions[index.row()] = {}
            self._portfolio_versions[index.row()]['id'] = value
            self.dataChanged.emit(index, index, self.__class__.IdentifierRole)
            return True
        elif index.isValid() and role == Qt.DisplayRole:
            self._portfolio_versions[index.row()] = {}
            self._portfolio_versions[index.row()]['name'] = value
            self.dataChanged.emit(index, index, Qt.DisplayRole)
            return True
        return False

    def load(self, portfolio_id):
        portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)
        if portfolio_result.is_err():
            print(portfolio_result.unwrap_err())
            return

        result = PortfolioVersionsListHandler().handle(portfolio=portfolio_result.unwrap())
        match result:
            case Ok(data):
                self._portfolio_versions = data
                for index, el in enumerate(data):
                    self.insertRow(index)
                    ix = self.index(index, index, QModelIndex())
                    self.setData(ix, el.id, self.__class__.IdentifierRole)
                    self.setData(ix, el.optimization_strategy_name, Qt.DisplayRole)
            case Err(error):
                self._portfolio_versions = []
                print(error)


