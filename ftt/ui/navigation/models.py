from PySide6.QtCore import QObject


class NavigationModel(QObject):
    def __init__(self):
        super().__init__()

        self._currentPortfolioId = None

    @property
    def currentPortfolioId(self):
        return self._currentPortfolioId

    @currentPortfolioId.setter
    def currentPortfolioId(self, value):
        self._currentPortfolioId = value
