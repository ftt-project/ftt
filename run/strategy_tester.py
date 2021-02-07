#!/usr/bin/env python

import fire
import backtrader as bt
import backtrader.analyzers as btanalyzers

from trade.configuration import Configuration
from trade.history_loader import HistoryLoader
from trade.logger import logger
from trade.strategies.bollinger_strategy import BollingerStrategy
from trade.strategies.macd_strategy import MACDStrategy
from trade.strategies.md_strategy import MDStrategy
from trade.strategies.sma_crossover_strategy import SMACrossoverStrategy
from trade.strategies.sma_strategy import SMAStrategy


def run():
    config = Configuration().scrape()

    datas = HistoryLoader.load_multiple(config.tickers, interval="1d")

    cerebro = bt.Cerebro()
    # cerebro.addstrategy(SMACrossoverStrategy, fast=5, slow=50)
    # cerebro.addstrategy(SMAStrategy)
    # cerebro.addstrategy(BollingerStrategy)
    # cerebro.addstrategy(MACDStrategy, atrdist=3.0)
    cerebro.addstrategy(MDStrategy)

    [cerebro.adddata(datas[key], name=key) for key in datas]
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcash(10000.0)

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(bt.analyzers.PyFolio)

    # # Add TimeReturn Analyzers for self and the benchmark data
    # cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='alltime_roi',
    #                     timeframe=bt.TimeFrame.NoTimeFrame)
    #
    # cerebro.addanalyzer(bt.analyzers.TimeReturn, data=data, _name='benchmark',
    #                     timeframe=bt.TimeFrame.NoTimeFrame)
    #
    # # Add TimeReturn Analyzers fot the annuyl returns
    # cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years)
    # # Add a SharpeRatio
    #  timeframe=bt.TimeFrame.Years,
    #                     riskfreerate=0.1)

    # Add SQN to qualify the trades
    cerebro.addanalyzer(bt.analyzers.SQN)
    cerebro.addobserver(bt.observers.DrawDown)  # visualize the drawdown evol


    logger.info("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
    thestrats = cerebro.run()

    # st0 = thestrats[0]
    # for alyzer in st0.analyzers:
    #     alyzer.print()

    logger.info("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
    sharpe = thestrats[0].analyzers.sharpe
    logger.info(f"Sharpe Ratio: {sharpe.get_analysis()}")

    sqn = thestrats[0].analyzers.sqn
    logger.info(f"SQN: {sqn.get_analysis()}")

    pyfolio = thestrats[0].analyzers.pyfolio
    returns, positions, transactions, gross_lev = pyfolio.get_pf_items()
    logger.info("Pyfolio returns:")
    logger.info(returns)
    logger.info("Pyfolio positions:")
    logger.info(positions)
    logger.info("Pyfolio transactions:")
    logger.info(transactions)
    cerebro.plot()


if __name__ == "__main__":
    fire.Fire(run)
