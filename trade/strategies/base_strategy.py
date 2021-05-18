from abc import abstractmethod

import backtrader as bt
from backtrader.feeds import DataBase

from trade.logger import logger
from trade.models import Order
from trade.repositories import OrdersRepository


class BaseStrategy(bt.Strategy):
    @abstractmethod
    def buy_signal(self, data: DataBase):
        pass

    @abstractmethod
    def sell_signal(self, data: DataBase):
        pass

    def after_buy(self, order: Order, data: DataBase):
        pass

    def after_sell(self, order: Order, data: DataBase):
        pass

    def after_next(self, data: DataBase):
        pass

    def start(self):
        self.orders = {}
        self.data_live = self.env.params.live

    def next(self):
        if not self.data_live:
            return

        for i, d in enumerate(self.datas):
            position = self.getposition(d).size

            if d._name in self.orders and self.orders[d._name]:
                return

            if not position:
                if self.buy_signal(d):
                    order = OrdersRepository().build_and_create(
                        symbol_name=d._name,
                        portfolio_version_id=self.p.portfolio_version_id,
                        desired_price=0,
                        type="buy",
                    )
                    btorder = self.buy(data=d)
                    logger.info("BUY CREATE, %.2f" % d.close[0])
                    self.orders[d._name] = btorder
                    self.orders[d._name].addinfo(d_name=d._name, order_id=order.id)
                    self.after_buy(order=order, data=d)
            else:
                if self.sell_signal(d):
                    order = OrdersRepository().build_and_create(
                        symbol_name=d._name,
                        portfolio_version_id=self.p.portfolio_version_id,
                        desired_price=0,
                        type="sell",
                    )
                    btorder = self.close(data=d)
                    self.orders[d._name] = btorder
                    self.after_sell(order=order, data=d)
                    self.orders[d._name].addinfo(d_name=d._name, order_id=order.id)
                else:
                    self.after_next(d)

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
