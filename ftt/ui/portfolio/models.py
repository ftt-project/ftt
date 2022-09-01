from PyQt6.QtCore import QObject, pyqtSignal


class PortfolioModel(QObject):
    portfolios_list_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._portfolios = []

    def get_portfolios(self):
        return [
            {
                "id": 1,
                "name": "Portfolio 1",
                "description": "The best portfolio",
            },
            {
                "id": 2,
                "name": "Portfolio 2",
                "description": "The second best portfolio",
            },
        ]

    def load_portfolios(self):
        self._portfolios = self.get_portfolios()
        self.portfolios_list_changed.emit()
