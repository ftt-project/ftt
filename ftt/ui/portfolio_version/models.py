from PySide6.QtCore import QObject


class PortfolioVersionModel(QObject):
    def __init__(self):
        super().__init__()
        self._portfolio_id = None
        self._portfolio_version_id = None

    def onPortfolioChanged(self, portfolio_id):
        self._portfolio_id = portfolio_id

    def onPortfolioVersionChanged(self, portfolio_version_id):
        self._portfolio_version_id = portfolio_version_id

    def getPortfolioVersionId(self):
        return self._portfolio_version_id

    def getPortfolioId(self):
        return self._portfolio_id