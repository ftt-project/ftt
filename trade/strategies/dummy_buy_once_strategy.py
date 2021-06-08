from trade.strategies.base_strategy import BaseStrategy


class DummyBuyOnceStrategy(BaseStrategy):
    params = (("portfolio_version_id", None),)

    def __init__(self):
        self.bought = False

    def buy_signal(self, data):
        if not self.bought:
            self.bought = True
            return True

        return False

    def sell_signal(self, data):
        return False

    def __str__(self):
        return "<DummyBuyOnceStrategy>"
