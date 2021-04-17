import backtrader as bt


class WeightsStrategy(bt.Strategy):
    def __init__(self):
        pass

    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            position = self.getposition(d).size
            self.buy(data=d)

