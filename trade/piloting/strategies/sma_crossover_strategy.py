import backtrader as bt
from trade.piloting.strategies.base_strategy import BaseStrategy


class SMACrossoverStrategy(BaseStrategy):
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

    def __str__(self):
        return "<SMACrossoverStrategy>"

    def buy_signal(self, data):
        return self.inds[data._name]["crossover"] < 0

    def sell_signal(self, data):
        return self.inds[data._name]["crossover"] > 0
