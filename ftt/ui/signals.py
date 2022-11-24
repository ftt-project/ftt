from PySide6.QtCore import QObject, Signal


class ApplicationSignals(QObject):
    welcomeScreenDisplayed = Signal()
    selectedPortfolioChanged = Signal(int)
    selectedPortfolioVersionChanged = Signal(int)
    newPortfolioDialogDisplayed = Signal()
    newPortfolioVersionDialogDisplayed = Signal()
    deletePortfolioVersionDialogDisplayed = Signal()
    addSecurityDialogDisplayed = Signal()
    selectedPortfolioVersionSecuritiesChanged = Signal()
    addSecurityDialogClosed = Signal()
