#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from datetime import datetime

import fire
import backtrader as bt


class St(bt.Strategy):
    def logdata(self):
        txt = []
        txt.append('{}'.format(len(self)))
        txt.append('{}'.format(self.data.datetime.datetime(0).isoformat()))
        txt.append('{:.2f}'.format(self.data.open[0]))
        txt.append('{:.2f}'.format(self.data.high[0]))
        txt.append('{:.2f}'.format(self.data.low[0]))
        txt.append('{:.2f}'.format(self.data.close[0]))
        txt.append('{:.2f}'.format(self.data.volume[0]))
        print(','.join(txt))

    data_live = False

    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)
        if status == data.LIVE:
            self.data_live = True

    # def notify_order(self, order):
    #     if order.status == order.Completed:
    #         buysell = 'BUY ' if order.isbuy() else 'SELL'
    #         txt = '{} {}@{}'.format(buysell, order.executed.size,
    #                                 order.executed.price)
    #         print(txt)

    bought = 0
    sold = 0

    def next(self):
        self.logdata()
        # if not self.data_live:
        #     return

        # if not self.bought:
        #     self.bought = len(self)  # keep entry bar
        #     print('buy')
        #     self.buy()
        # elif not self.sold:
        #     if len(self) == (self.bought + 3):
        #         print('sell')
        #         self.sell()


def run(args=None):
    cerebro = bt.Cerebro(stdstats=False)
    store = bt.stores.IBStore(port=7496, clientId=0)

    data = store.getdata(dataname='1H3-STK-SGX-SGD', timeframe=bt.TimeFrame.Ticks, compression=5,
                         fromdate=datetime.strptime('2021-01-13T00:00:00', '%Y-%m-%d' + 'T%H:%M:%S')
                         )

    cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=10)

    cerebro.broker = store.getbroker()

    cerebro.addstrategy(St)
    cerebro.run()


if __name__ == "__main__":
    fire.Fire(run)
