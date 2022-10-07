from PySide6.QtCore import QObject, Signal


class PortfolioSignals(QObject):
    portfolioChanged = Signal(int)
    portfolioVersionSelected = Signal(int)
    portfolioVersionInDBUpdated = Signal()
