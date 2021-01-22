#!/usr/bin/env python
from datetime import datetime

import fire
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd

from db.models import TickerReturn, Ticker
from db.configuration import database_connection
from trade.logger import logger
from trade.strategies.bollinger_strategy import BollingerStrategy

from trade.strategies.sma_crossover_strategy import SMACrossoverStrategy
from trade.strategies.sma_strategy import SMAStrategy


class PandasData(bt.feeds.PandasData):
    linesoverride = False  # discard usual OHLC structure
    # datetime must be present and last
    lines = ("close",)
    datafields = [
        "datetime",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    params = (
        ("datetime", None),
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
        ("adj_close", None),
        ("pct", "pct"),
        ("pct2", "pct2"),
        ("pct3", "pct3"),
    )


def load_data():
    query = (
        TickerReturn.select(
            TickerReturn.datetime,
            TickerReturn.open,
            TickerReturn.high,
            TickerReturn.low,
            TickerReturn.close,
            TickerReturn.volume,
        )
        .where(
            TickerReturn.ticker == Ticker.get(Ticker.ticker == "AAPL"),
            TickerReturn.interval == "1h",
        )
        .order_by(TickerReturn.datetime.asc())
    )

    dataframe = pd.read_sql(
        query.sql()[0],
        database_connection(),
        params=query.sql()[1],
        # parse_dates='datetime',
        index_col="datetime",
    )
    dataframe["pct"] = dataframe.close.pct_change(1)
    dataframe["pct2"] = dataframe.close.pct_change(5)
    dataframe["pct3"] = dataframe.close.pct_change(10)
    return dataframe


def data():
    return PandasData(dataname=load_data())


def run():
    cerebro = bt.Cerebro()
    # cerebro.addstrategy(SMACrossoverStrategy, fast=1, slow=5)
    # cerebro.addstrategy(SMAStrategy)
    cerebro.addstrategy(BollingerStrategy)
    cerebro.adddata(data())
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcash(10000.0)

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(bt.analyzers.PyFolio)

    logger.info("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
    thestrats = cerebro.run()
    logger.info("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
    sharpe = thestrats[0].analyzers.sharpe
    logger.info(f"Sharpe Ratio: {sharpe.get_analysis()}")

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
