#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from datetime import datetime

import fire
import backtrader as bt


class St(bt.Strategy):
    """
    Strategies playground
    """
    params = (("maperiod", 15), ("pfast", 9), ("pslow", 21))

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.order = None
        self.buyprice = None
        self.buycomm = None

        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

        self.sma = bt.indicators.MovingAverageSimple(
            self.dataclose, period=self.params.maperiod
        )

        # Plotting
        # bt.indicators.ExponentialMovingAverage(self.dataclose, period=25)
        # bt.indicators.WeightedMovingAverage(self.dataclose, period=25,
        #                                     subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0], plot=False)

    def log(self, txt, dt=None):
        """ Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def logdata(self):
        txt = []
        txt.append("{}".format(len(self)))
        txt.append("{}".format(self.data.datetime.datetime(0).isoformat()))
        txt.append("{:.2f}".format(self.data.open[0]))
        txt.append("{:.2f}".format(self.data.high[0]))
        txt.append("{:.2f}".format(self.data.low[0]))
        txt.append("{:.2f}".format(self.data.close[0]))
        txt.append("{:.2f}".format(self.data.volume[0]))
        print(",".join(txt))

    data_live = False

    def notify_data(self, data, status, *args, **kwargs):
        print("*" * 5, "DATA NOTIF:", data._getstatusname(status), *args)
        if status == data.LIVE:
            self.data_live = True

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log(
                    "SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm))

    bought = 0
    sold = 0

    # https://medium.com/@danjrod/interactive-brokers-in-python-with-backtrader-23dea376b2fc
    # multiple datas
    # https://backtest-rookies.com/2017/08/22/backtrader-multiple-data-feeds-indicators/
    def next(self):
        self.logdata()
        if not self.data_live:
            return

        if not self.bought:
            self.bought = len(self)
            self.log("BUY CREATE, %.2f" % self.dataclose[0])
            self.buy()
            self.sold = 0
        elif not self.sold:
            if len(self) == (self.bought + 3):
                self.log("SELL CREATE, %.2f" % self.dataclose[0])
                self.sell()
                self.bought = 0
        return

        self.logdata()

        if not self.data_live:
            print("Not live")
            return

        if self.order:
            print("Order exists")
            return

        if not self.position:
            if self.crossover > 0:
                self.log("BUY CREATE, %.2f" % self.dataclose[0])
                self.order = self.buy()
            else:
                self.log("crossover < 0")
        else:
            if self.crossover < 0:
                self.log("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()


def run(args=None):
    cerebro = bt.Cerebro(stdstats=False)
    store = bt.stores.IBStore(port=7497, clientId=0)

    data = store.getdata(
        dataname="1D3-STK-SGX-SGD",
        timeframe=bt.TimeFrame.Ticks,  # compression=5,
        rtbar=True,
        fromdate=datetime.strptime("2021-01-19T00:00:00", "%Y-%m-%d" + "T%H:%M:%S"),
    )

    cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=10)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    cerebro.broker = store.getbroker()

    cerebro.addstrategy(St)
    cerebro.run()
    # cerebro.plot()


if __name__ == "__main__":
    fire.Fire(run)
