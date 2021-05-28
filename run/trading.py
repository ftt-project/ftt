from datetime import datetime

import fire
import backtrader as bt

from trade.repositories import PortfoliosRepository
from trade.strategies import ValueProtectingStrategy, BollingerStrategy
from trade.strategies.sizers import WeightedSizer


def run(portfolio_id: int):
    cerebro = bt.Cerebro()
    store = bt.stores.IBStore(port=7497, clientId=1, host='127.0.0.1')

    portfolio = PortfoliosRepository.get_by_id(portfolio_id)
    tickers = PortfoliosRepository.get_tickers(portfolio)
    for ticker in tickers:
        data = store.getdata(
            dataname=ticker.symbol,
            sectype='STK',
            exchange='SMART',
            currency='USD',
            # timeframe=bt.TimeFrame.Minutes,
            # compression=5,
            rtbar=True,
            # fromdate=datetime.strptime("2021-05-26T00:00:00", "%Y-%m-%d" + "T%H:%M:%S"),
        )
        cerebro.resampledata(data, name=ticker.symbol, timeframe=bt.TimeFrame.Minutes, compression=5)
        # cerebro.replaydata(data, name=ticker.symbol, timeframe=bt.TimeFrame.Minutes, compression=5)

    cerebro.broker = store.getbroker()

    cerebro.addstrategy(ValueProtectingStrategy, portfolio_version_id=portfolio.id)
    # cerebro.addstrategy(BollingerStrategy, portfolio_version_id=portfolio.id)
    cerebro.addsizer(WeightedSizer)
    result = cerebro.run()


if __name__ == "__main__":
    fire.Fire(run)
