import backtrader as bt
from trade.logger import logger
from trade.repositories import OrdersRepository


class SMACrossoverStrategy(bt.Strategy):
    params = (
        ("portfolio_version_id", None),
        ("fast", 10),
        ("slow", 20),
        ("_movav", bt.indicators.SMA),
    )

    def __init__(self):
        self.inds = {}
        for i, d in enumerate(self.datas):
            self.inds[d._name] = {}

            sma_fast = self.p._movav(d.close, period=self.p.fast)
            sma_slow = self.p._movav(d.close, period=self.p.slow)
            self.inds[d._name]["crossover"] = bt.indicators.CrossOver(
                sma_fast, sma_slow
            )

    def start(self):
        self.orders = {}
        self.data_live = self.env.params.live

    def buy_sig(self, d_name):
        return self.inds[d_name]["crossover"] < 0

    def sell_sig(self, d_name):
        return self.inds[d_name]["crossover"] > 0

    def notify_order(self, order):
        order_id = order.info["order_id"]
        OrdersRepository().update_status(
            order_id=order_id, status=order.getstatusname()
        )

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

    def next(self):
        if not self.data_live:
            return

        for i, d in enumerate(self.datas):
            position = self.getposition(d).size

            if d._name in self.orders and self.orders[d._name]:
                return

            if not position:
                if self.buy_sig(d._name):
                    order = OrdersRepository().build_and_create(
                        symbol_name=d._name,
                        portfolio_version_id=self.p.portfolio_version_id,
                        desired_price=0,
                        type="buy",
                    )
                    logger.info("BUY CREATE, %.2f" % d.close[0])
                    self.orders[d._name] = self.buy(data=d)
                    self.orders[d._name].addinfo(d_name=d._name, order_id=order.id)
            else:
                if self.sell_sig(d._name):
                    order = OrdersRepository().build_and_create(
                        symbol_name=d._name,
                        portfolio_version_id=self.p.portfolio_version_id,
                        desired_price=0,
                        type="sell",
                    )
                    logger.info("SELL CREATE, %.2f" % d.close[0])
                    self.orders[d._name] = self.sell(data=d)
                    self.orders[d._name].addinfo(d_name=d._name, order_id=order.id)

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        logger.info(
            "OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm)
        )

    def notify_data(self, data, status, *args, **kwargs):
        logger.info(
            f"****** DATA NOTIF: {data._name} {data._getstatusname(status)}, {args}"
        )
        if status == data.LIVE or self.env.params.live:
            self.data_live = True
