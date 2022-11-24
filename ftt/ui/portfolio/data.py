from result import Ok, Err

from ftt.handlers.portfolio_load_handler import PortfolioLoadHandler
from ftt.handlers.portfolio_version_load_handler import PortfolioVersionLoadHandler
from ftt.handlers.portfolio_versions_list_handler import PortfolioVersionsListHandler
from ftt.handlers.weights_list_handler import WeightsListHandler


def getPortfolio(portfolio_id):
    portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)
    match portfolio_result:
        case Ok(portfolio):
            return portfolio
        case Err(error):
            print(f"getPortfolioVersions: Error: {error}")
            return


def getPortfolioVersions(portfolio_id):
    portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)
    match portfolio_result:
        case Err(error):
            print(f"getPortfolioVersions: Error: {error}")
            return

    portfolio_versions_result = PortfolioVersionsListHandler().handle(
        portfolio=portfolio_result.unwrap()
    )
    match portfolio_versions_result:
        case Ok(portfolio_versions):
            return portfolio_versions
        case Err(error):
            print(f"Error: {error}")
            return


def getPortfolioVersionWeights(portfolio_version_id):
    version_result = PortfolioVersionLoadHandler().handle(
        portfolio_version_id=portfolio_version_id
    )
    match version_result:
        case Err(error):
            print(
                f"getPortfolioVersionWeights: PortfolioVersionLoadHandler: Error: {error}"
            )
            return

    weights_result = WeightsListHandler().handle(
        portfolio_version=version_result.unwrap()
    )
    match weights_result:
        case Ok(weights):
            return weights
        case Err(error):
            print(f"getPortfolioVersionWeights: WeightsListHandler: Error: {error}")
            return


class ChangeCollectionIterator:
    def __init__(self, changes):
        self._changes = changes
        self._index = 0

    def __iter__(self):
        return self

    def __len__(self):
        return len(self._changes)

    def __next__(self):
        if self._index < len(self._changes):
            change = self._changes[self._index]
            self._index += 1
            return {
                "symbol": change[1].symbol,
                "delta": change[0].total_quantity,
                "operation": change[0].action.name,
                "amount": 0,
            }

        raise StopIteration


#
# class PortfolioModel(QObject):
#     def __init__(self):
#         super().__init__()
#
#         self._current_portfolio_version_changes = None
#         self._current_portfolio_version_id = None
#         self._current_portfolio_id = None
#         self._current_weights = None
#         self._current_portfolio_version = None
#         self._current_portfolio = None
#
#     # @property
#     # def currentPortfolioId(self):
#     #     return self._current_portfolio_id
#     #
#     # @currentPortfolioId.setter
#     # def currentPortfolioId(self, value):
#     #     self._current_portfolio_id = value
#
#     # @property
#     # def currentPortfolio(self):
#     #     return self._current_portfolio
#
#     @property
#     def currentPortfolioVersionId(self):
#         return self._current_portfolio_version_id
#
#     @currentPortfolioVersionId.setter
#     def currentPortfolioVersionId(self, value):
#         self._current_portfolio_version_id = value
#
#     @property
#     def currentPortfolioVersion(self):
#         return self._current_portfolio_version
#
#     @property
#     def currentPortfolioVersionChanges(self):
#         return self._current_portfolio_version_changes
#
#     @currentPortfolioVersionChanges.setter
#     def currentPortfolioVersionChanges(self, value):
#         self._current_portfolio_version_changes = ChangeCollectionIterator(value)