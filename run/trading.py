from datetime import datetime

import fire
import backtrader as bt

from trade.repositories import PortfoliosRepository
from trade.strategies.md_macd_strategy import MdMACDStrategy
from trade.strategies.sizers import WeightedSizer


def run():
    cerebro = bt.Cerebro()
    store = bt.stores.IBStore(port=7497, clientId=1, host='127.0.0.1')

    # portfolio = PortfoliosRepository().get_by_id(2)
    # tickers = PortfoliosRepository.get_tickers(portfolio)
    # for ticker in tickers:
    #     data = store.getdata(
    #         dataname=ticker.symbol,
    #         sectype='STK',
    #         exchange='SMART',
    #         # currency='USD',
    #         timeframe=bt.TimeFrame.Ticks,  # compression=5,
    #         rtbar=True,
    #         fromdate=datetime.strptime("2021-01-19T00:00:00", "%Y-%m-%d" + "T%H:%M:%S"),
    #     )
    #     cerebro.resampledata(data, name=ticker.symbol, timeframe=bt.TimeFrame.Seconds, compression=10)

    data = store.getdata(
        dataname="AAPL",
        sectype='STK',
        exchange='SMART', # NYSE
        currency='USD',
        timeframe=bt.TimeFrame.Ticks,
        # compression=5,
        rtbar=True,
        # fromdate=datetime.strptime("2021-01-19T00:00:00", "%Y-%m-%d" + "T%H:%M:%S"),
    )

    cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=10)

    cerebro.broker = store.getbroker()

    cerebro.addstrategy(MdMACDStrategy)
    cerebro.addsizer(WeightedSizer)
    result = cerebro.run()
    print(result)
    # cerebro.plot()


if __name__ == "__main__":
    fire.Fire(run)
