import backtrader as bt

from ftt.logger import logger


class SMAStrategy(bt.Strategy):
    params = (("period", 10),)

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.order = None

        self.sma = bt.indicators.MovingAverageSimple(
            self.dataclose, period=self.params.period
        )

    def __str__(self):
        return "<SMAStrategy>"

    def buy_sig(self):
        return (
            self.dataclose[0] > self.sma[0] and self.dataclose[-1] < self.dataclose[-2]
        )

    def sell_sig(self):
        return self.dataclose[0] < self.sma[0]

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                logger.info(
                    "BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

            else:
                logger.info(
                    "SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            logger.info("Order Canceled/Margin/Rejected")

        self.order = None

    def next(self):
        if self.order:
            return

        if len(self.position):
            if self.sell_sig():
                logger.info("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()
        else:
            if self.buy_sig():
                logger.info("BUY CREATE, %.2f" % self.dataclose[0])
                self.order = self.buy()
