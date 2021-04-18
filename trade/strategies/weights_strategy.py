import backtrader as bt


class WeightsStrategy(bt.Strategy):
    """
    TODO: Rename to WeightedStrategy
    TODO: Use it with SMA(?) or/and MD to buy stocks at the best time using Weighted Sizer
    """
    params = (("portfolio_id", None),)

    def __init__(self):
        pass

    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            position = self.getposition(d).size
            self.buy(data=d)
