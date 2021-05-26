from abc import abstractmethod

import backtrader as bt
from backtrader.feeds import DataBase

from trade.logger import logger
from trade.models import Order
from trade.repositories import (
    OrdersRepository,
    PortfolioVersionsRepository,
    TickersRepository,
    PortfoliosRepository,
    WeightsRepository,
)


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
        self._portfolio = PortfolioVersionsRepository.get_portfolio(
            self.p.portfolio_version_id
        )
        self.data_live = self.env.params.live

        tickers = PortfoliosRepository.get_tickers(self.portfolio)
        self._tickers = {}
        for ticker in tickers:
            self._tickers[ticker.symbol] = TickersRepository().get_by_name(
                ticker.symbol
            )

    @property
    def portfolio(self):
        return self._portfolio

    @property
    def tickers(self):
        return self._tickers

    def _open_order(self, symbol):
        return OrdersRepository.last_not_closed_order(
            self.portfolio, self.tickers[symbol]
        )

    def _open_order_exist(self, symbol):
        return self._open_order(symbol) is not None

    def next(self):
        if not self.data_live:
            return

        for i, d in enumerate(self.datas):
            position = self.getposition(d).size

            if self._open_order_exist(d._name):
                continue

            if not position:
                if self.buy_signal(d):
                    weight = WeightsRepository.find_by_ticker_and_portfolio(
                        ticker=TickersRepository().get_by_name(d._name),
                        portfolio_version_id=self.p.portfolio_version_id,
                    )
                    if weight.locked_at is not None:
                        logger.info(f"IS LOCKED <{d._name}> by {self}")
                        continue

                    order = OrdersRepository.build_and_create(
                        symbol_name=d._name,
                        portfolio_version_id=self.p.portfolio_version_id,
                        desired_price=d.close[0],
                        type="buy",
                    )
                    btorder = self.buy(data=d)
                    logger.info(f"BUY CREATE <{d._name}> by {self}, %.2f" % d.close[0])
                    self.orders[d._name] = btorder
                    self.orders[d._name].addinfo(d_name=d._name, order_id=order.id)
                    self.after_buy(order=order, data=d)
            else:
                if self.sell_signal(d):
                    order = OrdersRepository.build_and_create(
                        symbol_name=d._name,
                        portfolio_version_id=self.p.portfolio_version_id,
                        desired_price=d.close[0],
                        type="sell",
                    )
                    btorder = self.close(data=d)
                    logger.info(f"SELL CREATE <{d._name}> by {self}, %.2f" % d.close[0])
                    self.orders[d._name] = btorder
                    self.after_sell(order=order, data=d)
                    self.orders[d._name].addinfo(d_name=d._name, order_id=order.id)
                else:
                    self.after_next(d)

    def notify_order(self, order):
        order_id = order.info["order_id"]
        symbol = order.info["d_name"]
        OrdersRepository.update_status(order_id=order_id, status=order.getstatusname())

        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            OrdersRepository.set_execution_params(
                order=OrdersRepository.get_by_id(order_id),
                execution_size=order.executed.size,
                execution_price=order.executed.price,
                execution_value=order.executed.value,
                execution_commission=order.executed.comm,
            )
            if order.isbuy():
                weight = WeightsRepository.find_by_ticker_and_portfolio(
                    ticker=TickersRepository().get_by_name(symbol),
                    portfolio_version_id=self.p.portfolio_version_id,
                )
                WeightsRepository.update_amount(weight, order.executed.value)
                logger.info(
                    (
                        f"BUY EXECUTED <{order.info['d_name']}> by {self}, Price: {order.executed.price}, "
                        f"Cost: {order.executed.value}, Comm {order.executed.comm}"
                    )
                )

            else:
                weight = WeightsRepository.find_by_ticker_and_portfolio(
                    ticker=TickersRepository().get_by_name(symbol),
                    portfolio_version_id=self.p.portfolio_version_id,
                )
                WeightsRepository.update_amount(weight, 0)
                logger.info(
                    (
                        f"SELL EXECUTED <{order.info['d_name']}> by {self}, Price: {order.executed.price}, "
                        f"Cost: {order.executed.value}, Comm {order.executed.comm}"
                    )
                )
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            logger.info(f"Order {order.getstatusname()}")

        if not order.alive():
            d_name = order.info["d_name"]
            # TODO: Update order's status
            self.orders[d_name] = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        logger.info(
            f"OPERATION PROFIT by {self}, GROSS {trade.pnl}, NET {trade.pnlcomm}"
        )

    def notify_data(self, data, status, *args, **kwargs):
        logger.info(
            f"****** DATA NOTIF: {data._name} {data._getstatusname(status)}, {args}"
        )
        if status == data.LIVE or self.env.params.live:
            self.data_live = True
