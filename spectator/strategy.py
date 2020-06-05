from market.market import Market, Qoute

class StrategyAdviser(object):
    def __init__(self, symbol, enter_price, sell_price):
        self.symbol = symbol
        self.enter_price = enter_price

    def advised_to_exit(self):
        """
        Advised to exit to have the smallest loss
        """
        pass

    def advised_to_sell(self):
        """
        Advised to sell to have the biggest gains

        returns False when the current price haven't reach sell price
        returns True when the current price have reach sell price
        """
        qoute = Market.get_quote_endpoint(self.symbol)
        if qoute.price >= self.enter_price:
            return True
        else:
            return False
 
