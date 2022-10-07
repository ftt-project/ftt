from PySide6.QtCore import QObject, Signal
from result import Ok, Err

from ftt.handlers.portfolio_load_handler import PortfolioLoadHandler


class MainApplicationModel(QObject):
    """
    TODO: deprecate and remove
    """

    currentPortfolioChanged = Signal()
    currentPortfolioVersionsChanged = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._current_portfolio = None
        self._current_portfolio_versions = None

    def onPortfolioClicked(self, portfolio_id):
        print(f"Portfolio clicked: {portfolio_id}")

        portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)
        match portfolio_result:
            case Ok(portfolio):
                self._current_portfolio = portfolio
            case Err(error):
                print(f"Error: {error}")
                self._current_portfolio = None
                return
