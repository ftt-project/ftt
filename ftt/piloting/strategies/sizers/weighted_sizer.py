import backtrader as bt

# https://community.backtrader.com/topic/144/feature-request-allow-passing-of-data-object-to-sizer
from ftt.storage.repositories.securities_repository import SecuritiesRepository
from ftt.storage.repositories.weights_repository import WeightsRepository


class WeightedSizer(bt.Sizer):
    """
    TODO: Rename to WeightedSizer
    """

    params = (("dataname", None),)

    def _getsizing(self, comminfo, cash, data, isbuy):
        # portfolio = Portfolio.get_weights(self.p.dataname)
        # TODO: handle sell event
        ticker_name = data._name
        ticker = SecuritiesRepository().get_by_name(ticker_name)
        portfolio_version_id = self.strategy.params.portfolio_version_id

        weights = WeightsRepository().get_by_security_and_portfolio_version(
            portfolio_version_id=portfolio_version_id, security_id=ticker.id
        )

        self._data = self.strategy.getdatabyname(ticker_name)

        return weights.planned_position - weights.position
