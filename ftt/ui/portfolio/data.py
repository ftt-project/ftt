from result import Ok, Err

from ftt.handlers.portfolio_handlers import PortfolioLoadHandler
from ftt.handlers.portfolio_version_load_handler import PortfolioVersionLoadHandler
from ftt.handlers.weights_list_load_handler import WeightsListLoadHandler


def getPortfolio(portfolio_id):
    portfolio_result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)
    match portfolio_result:
        case Ok(portfolio):
            return portfolio
        case Err(error):
            print(f"getPortfolioVersions: Error: {error}")
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

    weights_result = WeightsListLoadHandler().handle(
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
