from PySide6.QtCore import QObject


class BacktestingModel(QObject):
    def __init__(self, portfolio_version_ids):
        super().__init__()
        self._portfolio_version_ids = portfolio_version_ids
        self._portfolio_versions = []
