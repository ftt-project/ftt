from PyQt6.QtCore import QAbstractListModel, Qt
from result import Ok

from ftt.handlers.portfolios_list_handler import PortfoliosListHandler


class NavigationModel(QAbstractListModel):
    def __init__(self, *args, portfolios=[], **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolios = portfolios
        
        if len(portfolios) == 0:
            result = PortfoliosListHandler().handle()
            match result:
                case Ok(portfolios):
                    self.portfolios = portfolios

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.portfolios[index.row()].name

    def rowCount(self, index):
        return len(self.portfolios)
