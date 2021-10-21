import backtrader as bt

from ftt.piloting.strategies.base_strategy import BaseStrategy


class MdMACDStrategy(BaseStrategy):
    params = (
        ("portfolio_version_id", None),
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
        self.pstop = {}
        self.data_live = self.env.params.live

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

    def __str__(self):
        return "<MdMACDStrategy>"

    def buy_signal(self, data) -> bool:
        return (
            self.inds[data._name]["cross_over"][0] > 0.0
            and self.inds[data._name]["smadir"] < 0.0
        )

    def sell_signal(self, data) -> bool:
        pclose = data.close[0]
        pstop = self.pstop[data._name]
        return pclose < pstop

    def after_buy(self, order, data) -> None:
        pdist = self.inds[data._name]["atr"][0] * self.p.atrdist
        self.pstop[data._name] = data.close[0] - pdist

    def after_next(self, data):
        pclose = data.close[0]
        pstop = self.pstop[data._name]
        pdist = self.inds[data._name]["atr"][0] * self.p.atrdist
        # Update only if greater than
        self.pstop[data._name] = max(pstop, pclose - pdist)
