import fire
import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
import pandas_datareader

from trade.models import TickerReturn, Ticker
from trade.base_command import BaseCommand
from trade.models import database_connection


class Analyze(BaseCommand):
    """
    Analyzer playground
    """
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

    class TestStrategy(bt.Strategy):
        params = (("maperiod", 15),)

        def log(self, txt, dt=None):
            """ Logging function for this strategy"""
            dt = dt or self.datas[0].datetime.date(0)
            print("%s, %s" % (dt.isoformat(), txt))

        def __init__(self):
            # Keep a reference to the "close" line in the data[0] dataseries
            self.dataclose = self.datas[0].close

            self.order = None
            self.buyprice = None
            self.buycomm = None

            # breakpoint()
            self.sma = bt.indicators.MovingAverageSimple(
                self.dataclose, period=self.params.maperiod
            )

            # Indicators for the plotting show
            bt.indicators.ExponentialMovingAverage(self.dataclose, period=25)
            bt.indicators.WeightedMovingAverage(self.dataclose, period=25, subplot=True)
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
                        "BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                        % (
                            order.executed.price,
                            order.executed.value,
                            order.executed.comm,
                        )
                    )

                    self.buyprice = order.executed.price
                    self.buycomm = order.executed.comm
                else:  # Sell
                    self.log(
                        "SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                        % (
                            order.executed.price,
                            order.executed.value,
                            order.executed.comm,
                        )
                    )

                self.bar_executed = len(self)

            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log("Order Canceled/Margin/Rejected")

            self.order = None

        def notify_trade(self, trade):
            if not trade.isclosed:
                return

            self.log(
                "OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm)
            )

        def next(self):
            # Simply log the closing price of the series from the reference
            self.log("Close, %.2f" % self.dataclose[0])

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
                        self.log("BUY CREATE, %.2f" % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.buy()

            else:

                # Already in the market ... we might sell
                if self.dataclose[0] < self.sma[0]:
                    # SELL, SELL, SELL!!! (with all possible default parameters)
                    self.log("SELL CREATE, %.2f" % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.sell()

    def playground(self):
        cerebro = bt.Cerebro()
        cerebro.addstrategy(Analyze.TestStrategy)
        data = Analyze.PandasData(dataname=self.__dataframe())
        cerebro.adddata(data)

        cerebro.addsizer(bt.sizers.FixedSize, stake=10)

        cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
        cerebro.addanalyzer(bt.analyzers.PyFolio)

        cerebro.broker.setcash(10000.0)

        print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
        thestrats = cerebro.run()
        print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
        sharpe = thestrats[0].analyzers.sharpe
        print("Sharpe Ratio:", sharpe.get_analysis())

        pyfolio = thestrats[0].analyzers.pyfolio
        returns, positions, transactions, gross_lev = pyfolio.get_pf_items()
        print("Pyfolio returns:")
        print(returns)
        print("Pyfolio positions:")
        print(positions)
        print("Pyfolio transactions:")
        print(transactions)
        cerebro.plot()

    def __dataframe(self):
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
                TickerReturn.ticker == Ticker.get(Ticker.ticker == "SHOP"),
                TickerReturn.interval == "1d",
            )
            .order_by(TickerReturn.datetime.asc())
        )

        # cur = database_connection().cursor()
        # raw_query = cur.mogrify(*query.sql())

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


if __name__ == "__main__":
    fire.Fire(Analyze)
