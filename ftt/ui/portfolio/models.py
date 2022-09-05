from PySide6.QtCore import QObject, Signal
from result import Ok, Err

from ftt.handlers.portfolio_load_handler import PortfolioLoadHandler
from ftt.handlers.portfolio_version_load_handler import PortfolioVersionLoadHandler
from ftt.handlers.portfolio_versions_list_handler import PortfolioVersionsListHandler
from ftt.handlers.weights_list_handler import WeightsListHandler


class PortfolioVersionsModel(QObject):
    portfolioVersionsListChanged = Signal()

    def __init__(self):
        super().__init__()

        self._current_weights = None
        self._current_portfolio_version = None
        self._current_portfolio = None
        self._current_portfolio_versions = None

    def getPortfolioVersions(self, portfolio_id):
        portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)
        match portfolio_result:
            case Ok(portfolio):
                self._current_portfolio = portfolio
            case Err(error):
                print(f"Error: {error}")
                self._current_portfolio = None
                return

        portfolio_versions_result = PortfolioVersionsListHandler().handle(portfolio=portfolio)
        match portfolio_versions_result:
            case Ok(portfolio_versions):
                self._current_portfolio_versions = portfolio_versions

            case Err(error):
                print(f"Error: {error}")
                return

        return self._current_portfolio_versions

    def getPortfolioVersionWeights(self, portfolio_version_id):
        version_result = PortfolioVersionLoadHandler().handle(portfolio_version_id=portfolio_version_id)
        match version_result:
            case Ok(version):
                self._current_portfolio_version = version
            case Err(error):
                print(f"Error: {error}")
                return

        weights_result = WeightsListHandler().handle(portfolio_version=self._current_portfolio_version)
        match weights_result:
            case Ok(weights):
                self._current_weights = weights
            case Err(error):
                print(f"Error: {error}")
                return

        return self._current_weights