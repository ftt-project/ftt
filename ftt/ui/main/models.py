from PySide6.QtCore import QAbstractListModel, Qt, QByteArray


class PortfoliosModel(QAbstractListModel):
    ValueRole = Qt.UserRole + 1

    def __init__(self):
        super().__init__()
        self._portfolios = []

    def roleNames(self):
        roles = {
            self.__class__.ValueRole: QByteArray(b'value'),
            Qt.DisplayRole: QByteArray(b'display')
        }
        return roles

    def rowCount(self, index):
        return len(self._portfolios)

    def data(self, index, role):
        d = self._portfolios[index.row()]

        if role == Qt.DisplayRole:
            return d['name']
        elif role == Qt.DecorationRole:
            return Qt.white
        elif role == self.__class__.ValueRole:
            return d['value']

        return None

    def populate(self, data=None):
        for item in data:
            self._portfolios.append(item)
