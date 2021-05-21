import pytest
import backtrader as bt

from trade.strategies.sizers import WeightedSizer


@pytest.fixture
def cerebro(portfolio_version, ticker, weight):
    def _cerebro(strategies, data):
        cerebro = bt.Cerebro(live=True, cheat_on_open=True)
        for strategy in strategies:
            cerebro.addstrategy(strategy, portfolio_version_id=portfolio_version.id)
        cerebro.addsizer(WeightedSizer)

        cerebro.adddata(data, name=ticker.symbol)

        cerebro.broker.setcash(30000.0)
        return cerebro

    return _cerebro
