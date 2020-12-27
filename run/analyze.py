import fire
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
from peewee import Value, SQL

from db.models import TickerReturn, Ticker
from trade.base_command import BaseCommand
from db.configuration import database_connection


class Analyze(BaseCommand):
    def simple(self):
        cerebro = bt.Cerebro(stdstats=False)
        cerebro.addanalyzer(bt.analyzers.PyFolio)
        cerebro.addstrategy(bt.Strategy)
        query = TickerReturn.select(
            TickerReturn.datetime,
            TickerReturn.open,
            TickerReturn.high,
            TickerReturn.low,
            TickerReturn.close,
            TickerReturn.volume,
            Value(-1).alias('openinterest')
        ).where(
            TickerReturn.ticker == Ticker.get(Ticker.ticker == 'SHOP'),
            TickerReturn.interval == '1d'
        )

        # cur = database_connection().cursor()
        # raw_query = cur.mogrify(*query.sql())

        dataframe = pd.read_sql(query.sql()[0], database_connection(),
                                params=query.sql()[1],
                                parse_dates='datetime',
                                index_col='datetime'
                                )
        data = bt.feeds.PandasData(dataname=dataframe)
        cerebro.adddata(data)
        result = cerebro.run()
        print(result[0])


if __name__ == "__main__":
    fire.Fire(Analyze)
