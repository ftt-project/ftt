import backtrader as bt

from trade.logger import logger


class MDStrategy(bt.Strategy):
    params = (
        ("oneplot", True),
        ("macd1", 6),
        ("macd2", 13),
        ("macdsig", 9),
        ("atrperiod", 14),
        ("atrdist", 3.0),
        ("smaperiod", 30),
        ("dirperiod", 10),
    )

    def __init__(self):
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.inds[d] = dict()
            macd = bt.indicators.MACD(
                d.close,
                period_me1=self.p.macd1,
                period_me2=self.p.macd2,
                period_signal=self.p.macdsig,
            )
            self.inds[d]["macd"] = macd
            cross_over = bt.indicators.CrossOver(macd.macd, macd.signal)
            self.inds[d]["cross_over"] = cross_over

            atr = bt.indicators.ATR(d, period=self.p.atrperiod)

            # Control market trend
            sma = bt.indicators.SMA(d, period=self.p.smaperiod)
            self.inds[d]["sma"] = sma

            smadir = sma - sma(-self.p.dirperiod)
            self.inds[d]["smadir"] = smadir

            if i > 0:
                if self.p.oneplot == True:
                    d.plotinfo.plotmaster = self.datas[0]

    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            position = self.getposition(d).size

            if self.order:
                return

            # if not self.position:  # not in the market
            #     if self.mcross[0] > 0.0 and self.smadir < 0.0:
            #         self.order = self.buy()
            #         pdist = self.atr[0] * self.p.atrdist
            #         self.pstop = self.data.close[0] - pdist
            #
            # else:  # in the market
            #     pclose = self.data.close[0]
            #     pstop = self.pstop
            #
            #     if pclose < pstop:
            #         self.close()  # stop met - get out
            #     else:
            #         pdist = self.atr[0] * self.p.atrdist
            #         # Update only if greater than
            #         self.pstop = max(pstop, pclose - pdist)

    def notify_trade(self, trade):
        dt = self.data.datetime.date()
        if trade.isclosed:
            print(
                "{} {} Closed: PnL Gross {}, Net {}".format(
                    dt, trade.data._name, round(trade.pnl, 2), round(trade.pnlcomm, 2)
                )
            )
