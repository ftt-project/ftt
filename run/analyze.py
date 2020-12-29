import fire
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import pyfolio as pf
import pandas_datareader
from peewee import Value, SQL

from db.models import TickerReturn, Ticker
from trade.base_command import BaseCommand
from db.configuration import database_connection
from trade.logger import logger


class Analyze(BaseCommand):
    class PandasData(bt.feeds.PandasData):
        linesoverride = False  # discard usual OHLC structure
        # datetime must be present and last
        lines = ('close',)
        datafields = [
            'datetime', 'open', 'high', 'low', 'close', 'volume',
        ]
        params = (
            ('datetime', None),
            ('open', 'open'),
            ('high', 'high'),
            ('low', 'low'),
            ('close', 'close'),
            ('volume', 'volume'),
            ('adj_close', None),
            ('pct', 'pct'),
            ('pct2', 'pct2'),
            ('pct3', 'pct3'),
        )

    class TestStrategy(bt.Strategy):
        params = (
            ('maperiod', 15),
        )

        def log(self, txt, dt=None):
            ''' Logging function for this strategy'''
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

        def __init__(self):
            # Keep a reference to the "close" line in the data[0] dataseries
            self.dataclose = self.datas[0].close
            bt.feeds.YahooFinanceCSVData
            self.order = None
            self.buyprice = None
            self.buycomm = None

            # breakpoint()
            self.sma = bt.indicators.MovingAverageSimple(self.dataclose, period=self.params.maperiod)

            # Indicators for the plotting show
            bt.indicators.ExponentialMovingAverage(self.dataclose, period=25)
            bt.indicators.WeightedMovingAverage(self.dataclose, period=25,
                                                subplot=True)
            bt.indicators.StochasticSlow(self.datas[0])
            bt.indicators.MACDHisto(self.datas[0])
            rsi = bt.indicators.RSI(self.datas[0])
            bt.indicators.SmoothedMovingAverage(rsi, period=10)
            bt.indicators.ATR(self.datas[0], plot=False)

        def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                # Buy/Sell order submitted/accepted to/by broker - Nothing to do
                return

            # Check if an order has been completed
            # Attention: broker could reject order if not enough cash
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log(
                        'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                        (order.executed.price,
                         order.executed.value,
                         order.executed.comm))

                    self.buyprice = order.executed.price
                    self.buycomm = order.executed.comm
                else:  # Sell
                    self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                             (order.executed.price,
                              order.executed.value,
                              order.executed.comm))

                self.bar_executed = len(self)

            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log('Order Canceled/Margin/Rejected')

            self.order = None

        def notify_trade(self, trade):
            if not trade.isclosed:
                return

            self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                     (trade.pnl, trade.pnlcomm))

        def next(self):
            # Simply log the closing price of the series from the reference
            self.log('Close, %.2f' % self.dataclose[0])

            # Check if an order is pending ... if yes, we cannot send a 2nd one
            if self.order:
                return

            # Check if we are in the market
            if not self.position:

                # Not yet ... we MIGHT BUY if ...
                if self.dataclose[0] > self.sma[0]:
                    # current close less than previous close

                    if self.dataclose[-1] < self.dataclose[-2]:
                        # previous close less than the previous close

                        # BUY, BUY, BUY!!! (with default parameters)
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.buy()

            else:

                # Already in the market ... we might sell
                if self.dataclose[0] < self.sma[0]:
                    # SELL, SELL, SELL!!! (with all possible default parameters)
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.sell()

    def playground(self):
        cerebro = bt.Cerebro()
        cerebro.addstrategy(Analyze.TestStrategy)
        data = Analyze.PandasData(dataname=self.__dataframe())
        cerebro.adddata(data)
        cerebro.broker.setcash(10000.0)
        cerebro.addsizer(bt.sizers.FixedSize, stake=10)
        cerebro.broker.setcommission(commission=0.0)
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.plot()

    def simple(self):
        data = Analyze.PandasData(dataname=self.__dataframe())

        cerebro = bt.Cerebro(stdstats=False)
        cerebro.broker.set_cash(100000)
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
        # cerebro.addstrategy(bt.Strategy)
        cerebro.addstrategy(Analyze.TestStrategy)
        cerebro.adddata(data)
        result = cerebro.run()

        strat = result[0]
        print(result[0])

        pyfolio = strat.analyzers.getbyname('pyfolio')

        returns, positions, transactions, gross_lev = pyfolio.get_pf_items()
        print(returns)
        pf.create_full_tear_sheet(
            returns,
            positions=positions,
            transactions=transactions,
            live_start_date='2019-10-02',  # This date is sample specific
            round_trips=True
        )

    def __dataframe(self):
        query = TickerReturn.select(
            TickerReturn.datetime,
            TickerReturn.open,
            TickerReturn.high,
            TickerReturn.low,
            TickerReturn.close,
            TickerReturn.volume
        ).where(
            TickerReturn.ticker == Ticker.get(Ticker.ticker == 'SHOP'),
            TickerReturn.interval == '1d'
        )

        # cur = database_connection().cursor()
        # raw_query = cur.mogrify(*query.sql())

        dataframe = pd.read_sql(query.sql()[0], database_connection(),
                                params=query.sql()[1],
                                # parse_dates='datetime',
                                index_col='datetime'
                                )
        dataframe['pct'] = dataframe.close.pct_change(1)
        dataframe['pct2'] = dataframe.close.pct_change(5)
        dataframe['pct3'] = dataframe.close.pct_change(10)
        return dataframe


if __name__ == "__main__":
    fire.Fire(Analyze)
