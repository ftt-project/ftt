import backtrader as bt

# https://community.backtrader.com/topic/144/feature-request-allow-passing-of-data-object-to-sizer
from trade.repositories import TickersRepository, WeightsRepository


class WeightedSizer(bt.Sizer):
    """
    TODO: Rename to WeightedSizer
    """

    params = (("dataname", None), ("portfolio_version_id", None))

    def _getsizing(self, comminfo, cash, data, isbuy):
        # portfolio = Portfolio.get_weights(self.p.dataname)
        # TODO: handle sell event
        ticker_name = data._name
        ticker = TickersRepository().get_by_name(ticker_name)
        portfolio_version_id = self.strategy.params.portfolio_version_id

        weights = WeightsRepository().get_by_ticker_and_portfolio_version(
            portfolio_version_id=portfolio_version_id, ticker_id=ticker.id
        )

        self._data = self.strategy.getdatabyname(ticker_name)

        return weights.planned_position - weights.position
