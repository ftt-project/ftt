from PySide6.QtCore import QAbstractListModel, Qt, QByteArray, Slot, Signal
from result import Ok, Err

from ftt.handlers.portfolios_list_handler import PortfoliosListHandler


class PortfoliosModel(QAbstractListModel):
    selectionChanged = Signal(int)

    IdentifierRole = Qt.UserRole + 1
    # ValueRole = Qt.UserRole + 1

    def __init__(self):
        super().__init__()
        self._portfolios = []

    def roleNames(self):
        roles = {
            # self.__class__.ValueRole: QByteArray(b'value'),
            self.__class__.IdentifierRole: QByteArray(b'identifier'),
            Qt.DisplayRole: QByteArray(b'display')
        }
        return roles

    def rowCount(self, index):
        return len(self._portfolios)

    def data(self, index, role):
        d = self._portfolios[index.row()]

        if role == Qt.DisplayRole:
            return d.name
        elif role == self.__class__.IdentifierRole:
            return d.id
        # elif role == Qt.DecorationRole:
        #     return Qt.white
        # elif role == self.__class__.ValueRole:
        #     return d['value']

        return None

    def load(self):
        result = PortfoliosListHandler().handle()
        match result:
            case Ok(data):
                self._portfolios = data
            case Err(error):
                print(error)

    @Slot(int)
    def selectPortfolio(self, portfolio_id) -> None:
        print("selectPortfolio", portfolio_id)
        self.selectionChanged.emit(portfolio_id)
