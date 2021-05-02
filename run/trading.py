from datetime import datetime

import fire
import backtrader as bt

from trade.logger import logger
from trade.models import Portfolio
from trade.strategies.md_macd_strategy import MdMACDStrategy
from trade.strategies.sizers import WeightedPortfolioSizer


def run():
    cerebro = bt.Cerebro(stdstats=False)
    store = bt.stores.IBStore(port=7497, clientId=0)

    portfolio = Portfolio.get_by_id(1)
    for weight in portfolio.weights:
        ticker = weight.ticker
        dataname = f"{ticker.name}-STK-{ticker.exchange}"
        data = store.getdata(
            dataname=dataname,
            timeframe=bt.TimeFrame.Ticks,  # compression=5,
            rtbar=True,
            fromdate=datetime.strptime("2021-01-19T00:00:00", "%Y-%m-%d" + "T%H:%M:%S"),
        )
        cerebro.resampledata(data, name=ticker.name, timeframe=bt.TimeFrame.Seconds, compression=10)

    cerebro.broker = store.getbroker()

    cerebro.addstrategy(MdMACDStrategy)
    cerebro.addsizer(WeightedPortfolioSizer)
    result = cerebro.run()
    # cerebro.plot()


if __name__ == "__main__":
    fire.Fire(run)
