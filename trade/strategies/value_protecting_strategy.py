from decimal import Decimal

from trade.logger import logger
from trade.repositories import WeightsRepository, TickersRepository
from trade.strategies.base_strategy import BaseStrategy


class ValueProtectingStrategy(BaseStrategy):
    params = (
        ("portfolio_version_id", -1),
        ("dipmult", 0.97),
    )

    def __str__(self):
        return f"<ValueProtectingStrategy>"

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
        broker = self.env.getbroker()
        value = broker.get_value(datas=[data])
        ticker = TickersRepository().get_by_name(data._name)
        weight = WeightsRepository.find_by_ticker_and_portfolio(
            ticker=ticker, portfolio_version_id=self.p.portfolio_version_id
        )
        return value <= (weight.amount * Decimal(self.p.dipmult))
