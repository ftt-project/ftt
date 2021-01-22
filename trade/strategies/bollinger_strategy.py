import backtrader as bt
from trade.logger import logger


class BollingerStrategy(bt.Strategy):
    params = (("period", 20), ("devfactor", 2.0), ("size", 20), ("debug", False))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.boll = bt.indicators.BollingerBands(
            self.dataclose, period=self.p.period, devfactor=self.p.devfactor
        )

        self.redline = None
        self.blueline = None

    def buy_sig(self):
        pass

    def sell_sig(self):
        pass

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

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        logger.info(
            "OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm)
        )

    def next(self):
        if self.order:
            return

        if self.dataclose < self.boll.lines.bot and not self.position:
            self.redline = True

        if self.dataclose > self.boll.lines.top and self.position:
            self.blueline = True

        if self.dataclose > self.boll.lines.mid and not self.position and self.redline:
            logger.info("BUY CREATE, %.2f" % self.dataclose[0])
            self.order = self.buy()

        if self.dataclose > self.boll.lines.top and not self.position:
            logger.info("BUY CREATE, %.2f" % self.dataclose[0])
            self.order = self.buy()

        if self.dataclose < self.boll.lines.mid and self.position and self.blueline:
            logger.info("SELL CREATE, %.2f" % self.dataclose[0])
            self.blueline = False
            self.redline = False
            self.order = self.sell()

    def next2(self):
        if self.order:
            return
        # orders = self.broker.get_orders_open()

        # Cancel open orders so we can track the median line
        # if orders:
        #     for order in orders:
        #         self.broker.cancel(order)

        if not self.position:
            if self.data.close > self.boll.lines.top:
                self.order = self.sell(
                    exectype=bt.Order.Stop, price=self.boll.lines.top[0]
                )  # , size=self.p.size)

            if self.data.close < self.boll.lines.bot:
                self.order = self.buy(
                    exectype=bt.Order.Stop, price=self.boll.lines.bot[0]
                )

        else:

            if self.position.size > 0:
                self.order = self.sell(
                    exectype=bt.Order.Limit, price=self.boll.lines.mid[0]
                )

            else:
                self.order = self.buy(
                    exectype=bt.Order.Limit, price=self.boll.lines.mid[0]
                )
