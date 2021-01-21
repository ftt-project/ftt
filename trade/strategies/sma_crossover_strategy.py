import backtrader as bt
from trade.logger import logger


class SMACrossoverStrategy(bt.Strategy):
    params = (
        ('fast', 10),
        ('slow', 30),
        ('_movav', bt.indicators.MovAv.SMA)
    )

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.order = None

        sma_fast = self.p._movav(self.dataclose, period=self.p.fast)
        sma_slow = self.p._movav(self.dataclose, period=self.p.slow)

        self.crossover = bt.indicators.CrossOver(sma_fast, sma_slow)

    def buy_sig(self):
        return self.crossover < 0

    def sell_sig(self):
        return self.crossover > 0

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                logger.info(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:
                logger.info('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            logger.info('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        if self.order:
            return

        if len(self.position):
            if self.sell_sig():
                logger.info('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()
        else:
            if self.buy_sig():
                logger.info('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()


