from decimal import Decimal

from trade.repositories import PortfolioVersionsRepository
from trade.strategies.base_strategy import BaseStrategy


class ValueProtectingStrategy(BaseStrategy):
    params = (
        ("portfolio_version_id", -1),
        ("dipmult", 0.96),
    )

    def buy_signal(self, data):
        """
        Buys when the dip is gone. Criteria
        - price is more or equal to the last sell price
        - uptrend of the stock
        """
        pass

    def sell_signal(self, data):
        """
        To protect from dip it sells when the portfolio price becomes lower than VALUE * MULT
        """
        portfolio = PortfolioVersionsRepository().get_portfolio(
            self.p.portfolio_version_id
        )
        broker = self.env.getbroker()
        value = broker.get_value()
        return value <= (portfolio.size * Decimal(self.p.dipmult))
