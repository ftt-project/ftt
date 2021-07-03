from decimal import Decimal

from trade.piloting.strategies.base_strategy import BaseStrategy
from trade.storage.repositories import SecuritiesRepository, WeightsRepository


class ValueProtectingStrategy(BaseStrategy):
    params = (
        ("portfolio_version_id", -1),
        ("buy_enabled", False),
        ("dipmult", 0.97),
    )

    def __str__(self):
        return "<ValueProtectingStrategy>"

    def buy_signal(self, data):
        """
        Buys when the dip is gone. Criteria
        - price is more or equal to the last sell price
        - uptrend of the stock
        """
        weight = WeightsRepository.find_by_security_and_portfolio(
            security=SecuritiesRepository().get_by_name(data._name),
            portfolio_version_id=self.p.portfolio_version_id,
        )
        if weight.locked_at_amount and data.close[0] >= weight.locked_at_amount:
            WeightsRepository.unlock_weight(weight=weight)
            if self.p.buy_enabled:
                return True

        return False

    def sell_signal(self, data):
        """
        To protect from dip it sells when the portfolio price becomes lower than VALUE * MULT
        """
        value = data.close[0]
        security = SecuritiesRepository().get_by_name(data._name)
        weight = WeightsRepository.find_by_security_and_portfolio(
            security=security, portfolio_version_id=self.p.portfolio_version_id
        )
        return value <= (weight.peaked_value * Decimal(self.p.dipmult))

    def after_sell(self, order, data):
        """
        TODO: Should it be after order is executed?
        """
        weight = WeightsRepository.find_by_security_and_portfolio(
            security=SecuritiesRepository().get_by_name(data._name),
            portfolio_version_id=self.p.portfolio_version_id,
        )
        WeightsRepository.lock_weight(weight=weight, locked_at_amount=data.close[0])
