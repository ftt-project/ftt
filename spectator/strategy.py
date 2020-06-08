from market.market import Market

class StrategyAdviser(object):
    def __init__(self, symbol, enter_price, sell_price, loss_threshold_percent):
        self.symbol = symbol
        self.enter_price = enter_price
        self.loss_threshold_percent = loss_threshold_percent

    def advised_to_exit(self):
        """
        Advised to exit to have the smallest loss

        return True when current price is lower when enter price minus loss threshold
        return False when current price is in the threshold range
        """
        minimal_acceptanble_price = self.enter_price - (self.enter_price / 100 * self.loss_threshold_percent)
        qoute = Market().get_quote_endpoint(self.symbol)

        if minimal_acceptanble_price >= qoute.price:
            return True
        else:
            return False

    def advised_to_sell(self):
        """
        Advised to sell to have the biggest gains

        returns False when the current price haven't reach sell price
        returns True when the current price have reach sell price
        """
        qoute = Market().get_quote_endpoint(self.symbol)
        if qoute.price >= self.enter_price:
            return True
        else:
            return False

