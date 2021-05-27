import backtrader as bt
from trade.strategies.base_strategy import BaseStrategy


class BollingerStrategy(BaseStrategy):
    params = (
        ("portfolio_version_id", None),
        ("period", 20),
        ("fast", 10),
        ("slow", 20),
        ("devfactor", 2.0),
    )

    def __init__(self):
        self.inds = {}
        for i, data in enumerate(self.datas):
            self.inds[data._name] = {}

            self.inds[data._name]["boll"] = bt.indicators.BollingerBands(
                data.close, period=self.p.period, devfactor=self.p.devfactor
            )

            # self.inds[data._name]["redline"] = None
            # self.inds[data._name]["blueline"] = None

    def __str__(self):
        return f"<BollingerStrategy>"

    def buy_signal(self, data):
        redline = data.close[0] < self.inds[data._name]["boll"].lines.bot
        return (
            data.close[0] > self.inds[data._name]["boll"].lines.mid and redline
        ) or (data.close[0] > self.inds[data._name]["boll"].lines.top)

    def sell_signal(self, data):
        blueline = data.close[0] > self.inds[data._name]["boll"].lines.top
        return (
            (data.close[0] < self.inds[data._name]["boll"].lines.mid)
            or blueline
            # and self.inds[data._name]["blueline"]
            # and blueline
        )

    # def after_sell(self, order, data):
    #     self.inds[data._name]["blueline"] = False
    #     self.inds[data._name]["redline"] = False

    # def next_old(self):
    #     if self.orders:
    #         return
    #
    #     if self.dataclose < self.boll.lines.bot and not self.position:
    #         self.redline = True
    #
    #     if self.dataclose > self.boll.lines.top and self.position:
    #         self.blueline = True
    #
    #     if self.dataclose > self.boll.lines.mid and not self.position and self.redline:
    #         logger.info("BUY CREATE, %.2f" % self.dataclose[0])
    #         self.order = self.buy()
    #
    #     if self.dataclose > self.boll.lines.top and not self.position:
    #         logger.info("BUY CREATE, %.2f" % self.dataclose[0])
    #         self.order = self.buy()
    #
    #     if self.dataclose < self.boll.lines.mid and self.position and self.blueline:
    #         logger.info("SELL CREATE, %.2f" % self.dataclose[0])
    #         self.blueline = False
    #         self.redline = False
    #         self.order = self.sell()

    # def next2(self):
    #     if self.order:
    #         return
    #     # orders = self.broker.get_orders_open()
    #
    #     # Cancel open orders so we can track the median line
    #     # if orders:
    #     #     for order in orders:
    #     #         self.broker.cancel(order)
    #
    #     if not self.position:
    #         if self.data.close > self.boll.lines.top:
    #             self.order = self.sell(
    #                 exectype=bt.Order.Stop, price=self.boll.lines.top[0]
    #             )  # , size=self.p.size)
    #
    #         if self.data.close < self.boll.lines.bot:
    #             self.order = self.buy(
    #                 exectype=bt.Order.Stop, price=self.boll.lines.bot[0]
    #             )
    #
    #     else:
    #
    #         if self.position.size > 0:
    #             self.order = self.sell(
    #                 exectype=bt.Order.Limit, price=self.boll.lines.mid[0]
    #             )
    #
    #         else:
    #             self.order = self.buy(
    #                 exectype=bt.Order.Limit, price=self.boll.lines.mid[0]
    #             )
