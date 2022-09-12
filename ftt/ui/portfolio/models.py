from PySide6.QtCore import QObject, Signal
from result import Ok, Err

from ftt.handlers.portfolio_load_handler import PortfolioLoadHandler
from ftt.handlers.portfolio_version_load_handler import PortfolioVersionLoadHandler
from ftt.handlers.portfolio_versions_list_handler import PortfolioVersionsListHandler
from ftt.handlers.weights_list_handler import WeightsListHandler


model = None


def get_model():
    global model
    if model is None:
        model = PortfolioModel()
    return model


class PortfolioModel(QObject):
    def __init__(self):
        super().__init__()

        self._current_portfolio_version_id = None
        self._current_portfolio_id = None
        self._current_weights = None
        self._current_portfolio_version = None
        self._current_portfolio = None

    @property
    def currentPortfolioId(self):
        return self._current_portfolio_id

    @currentPortfolioId.setter
    def currentPortfolioId(self, value):
        self._current_portfolio_id = value

    @property
    def currentPortfolio(self):
        return self._current_portfolio

    # @currentPortfolio.setter
    # def currentPortfolio(self, value):
    #     self.signals.portfolioChanged.emit()
    #     self._current_portfolio = value

    @property
    def currentPortfolioVersionId(self):
        return self._current_portfolio_version_id

    @currentPortfolioVersionId.setter
    def currentPortfolioVersionId(self, value):
        self._current_portfolio_version_id = value

    @property
    def currentPortfolioVersion(self):
        return self._current_portfolio_version

    # @currentPortfolioVersion.setter
    # def currentPortfolioVersion(self, value):
    #     self._current_portfolio_version = value

    def getPortfolio(self, portfolio_id):
        portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)
        match portfolio_result:
            case Ok(portfolio):
                return portfolio
            case Err(error):
                print(f"getPortfolio: Error: {error}")
                return None

    def getPortfolioVersions(self):
        portfolio_result = PortfolioLoadHandler().handle(portfolio_id=self.currentPortfolioId)
        match portfolio_result:
            case Ok(portfolio):
                self._current_portfolio = portfolio
            case Err(error):
                print(f"getPortfolioVersions: Error: {error}")
                self._current_portfolio = None
                return

        portfolio_versions_result = PortfolioVersionsListHandler().handle(portfolio=self.currentPortfolio)
        match portfolio_versions_result:
            case Ok(portfolio_versions):
                return portfolio_versions
            case Err(error):
                print(f"Error: {error}")
                return

    def getPortfolioVersionWeights(self):
        print(__file__, f"{self.currentPortfolioVersionId}")
        version_result = PortfolioVersionLoadHandler().handle(
            portfolio_version_id=self.currentPortfolioVersionId
        )
        match version_result:
            case Ok(version):
                self._current_portfolio_version = version
            case Err(error):
                print(f"getPortfolioVersionWeights: PortfolioVersionLoadHandler: Error: {error}")
                return

        weights_result = WeightsListHandler().handle(portfolio_version=self.currentPortfolioVersion)
        match weights_result:
            case Ok(weights):
                self._current_weights = weights
            case Err(error):
                print(f"getPortfolioVersionWeights: WeightsListHandler: Error: {error}")
                return
        return self._current_weights
