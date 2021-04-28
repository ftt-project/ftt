import backtrader as bt

from trade.logger import logger


class MdMACDStrategy(bt.Strategy):
    params = (
        ("portfolio_id", None),
        # Standard MACD Parameters
        ("macd1", 6),
        ("macd2", 13),
        ("macdsig", 9),
        ("atrperiod", 14),  # ATR Period (standard)
        ("atrdist", 3.0),  # ATR distance for stop price
        ("smaperiod", 30),  # SMA Period (pretty standard)
        ("dirperiod", 10),  # Lookback period to consider SMA trend direction
    )

    def __init__(self):
        self.inds = {}
        for i, d in enumerate(self.datas):
            self.inds[d._name] = {}

            macd = bt.indicators.MACD(
                d.close,
                period_me1=self.p.macd1,
                period_me2=self.p.macd2,
                period_signal=self.p.macdsig,
            )
            self.inds[d._name]["macd"] = macd

            # Cross of macd.macd and macd.signal
            cross_over = bt.indicators.CrossOver(macd.macd, macd.signal)
            self.inds[d._name]["cross_over"] = cross_over

            # To set the stop price
            atr = bt.indicators.ATR(d, period=self.p.atrperiod)
            self.inds[d._name]["atr"] = atr

            # Control market trend
            sma = bt.indicators.SMA(d.close, period=self.p.smaperiod)
            smadir = sma - sma(-self.p.dirperiod)
            self.inds[d._name]["smadir"] = smadir


    def start(self):
        self.orders = {}
        self.pstop = {}

    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            position = self.getposition(d).size

            if d._name in self.orders and self.orders[d._name]:
                return

            if not position:  # not in the market
                if self.inds[d._name]["cross_over"][0] > 0.0 and self.inds[d._name]["smadir"] < 0.0:
                    self.orders[d._name] = self.buy(data=d)
                    self.orders[d._name].addinfo(d_name=d._name)
                    pdist = self.inds[d._name]["atr"][0] * self.p.atrdist
                    self.pstop[d._name] = d.close[0] - pdist

            else:  # in the market
                pclose = d.close[0]
                pstop = d._name in self.pstop

                if pclose < pstop:
                    self.orders[d._name] = self.close(data=d)  # stop met - get out
                    self.orders[d._name].addinfo(d_name=d._name)
                else:
                    pdist = self.inds[d._name]["atr"][0] * self.p.atrdist
                    # Update only if greater than
                    self.pstop[d._name] = max(pstop, pclose - pdist)

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

        if not order.alive():
            d_name = order.info["d_name"]
            self.orders[d_name] = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        logger.info(
            "OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm)
        )
