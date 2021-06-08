#!/usr/bin/env python
from collections import OrderedDict
from datetime import date, datetime

import fire
import backtrader as bt
import backtrader.analyzers as btanalyzers

from trade.configuration import Configuration
from trade.models import Portfolio
from trade.history_loader import HistoryLoader
from trade.logger import logger
from trade.observers import PeakObserver
from trade.repositories import PortfolioVersionsRepository, PortfoliosRepository
from trade.strategies import ValueProtectingStrategy
from trade.strategies.bollinger_strategy import BollingerStrategy
from trade.strategies.dummy_buy_once_strategy import DummyBuyOnceStrategy
from trade.strategies.macd_strategy import MACDStrategy
from trade.strategies.md_macd_strategy import MdMACDStrategy
from trade.strategies.sizers import WeightedSizer
from trade.strategies.sma_crossover_strategy import SMACrossoverStrategy
from trade.strategies.sma_strategy import SMAStrategy

class IBCommision(bt.CommInfoBase):

    """A :class:`IBCommision` charges the way interactive brokers does.
    https://community.backtrader.com/topic/1008/how-to-build-a-commission-model-for-interactive-brokers-ib
    """

    params = (
        #('stocklike', True),
        #('commtype', bt.CommInfoBase.COMM_PERC),
        #('percabs', True),

        # Float. The amount charged per share. Ex: 0.005 means $0.005
        ('per_share', 0.005),

        # Float. The minimum amount that will be charged. Ex: 1.0 means $1.00
        ('min_per_order', 1.0),

        # Float. The maximum that can be charged as a percent of the trade value. Ex: 0.005 means 0.5%
        ('max_per_order_abs_pct', 0.005),
    )

    def _getcommission(self, size, price, pseudoexec):

        """
        :param size: current position size. > 0 for long positions and < 0 for short positions (this parameter will not be 0)
        :param price: current position price
        :param pseudoexec:
        :return: the commission of an operation at a given price
        """

        commission = size * self.p.per_share
        order_price = price * size
        commission_as_percentage_of_order_price = commission / order_price

        if commission < self.p.min_per_order:
            commission = self.p.min_per_order
        elif commission_as_percentage_of_order_price > self.p.max_per_order_abs_pct:
            commission = order_price * self.p.max_per_order_abs_pct
        return commission


def run(portfolio_id: int) -> None:
    """
    Parameters:
        portfolio_id: Portfolio to use

    Bollinger                               10436.71
    SMACrossoverStrategy                    10726.09
    SMAStrategy                             10239.02
    MACDStrategy                            11425.63
    MdMACDStrategy                          14910.82
    MdMACDStrategy[WeightedPortfolioSizer]  17834.67
    """
    portfolio = PortfoliosRepository.get_by_id(portfolio_id)
    portfolio_version = PortfolioVersionsRepository().get_latest_version(portfolio.id)

    cerebro = bt.Cerebro(live=True, cheat_on_open=True)
    # cerebro.addstrategy(SMACrossoverStrategy, fast=5, slow=50)
    # cerebro.addstrategy(SMAStrategy)
    # cerebro.addstrategy(BollingerStrategy)
    # cerebro.addstrategy(MACDStrategy, atrdist=3.0)
    # cerebro.addstrategy(MDStrategy)
    cerebro.addstrategy(BollingerStrategy, portfolio_version_id=portfolio_version.id)
    # cerebro.addstrategy(DummyBuyOnceStrategy, portfolio_version_id=portfolio_version.id)
    # cerebro.addstrategy(ValueProtectingStrategy, portfolio_version_id=portfolio_version.id, dipmult=1.0, buy_enabled=False)

    tickers = PortfoliosRepository.get_tickers(portfolio)
    for ticker in tickers:
        data = HistoryLoader.load(ticker, datetime(2021, 5, 1, 0, 0, 0), datetime(2021, 5, 13, 23, 59, 59), interval="5m")
        cerebro.adddata(data, name=ticker.symbol)
        # cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=5)

    cerebro.addsizer(WeightedSizer)
    cerebro.broker.setcash(float(portfolio.amount))

    comminfo = IBCommision()
    cerebro.broker.addcommissioninfo(comminfo)

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
    cerebro.addobserver(PeakObserver)

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
