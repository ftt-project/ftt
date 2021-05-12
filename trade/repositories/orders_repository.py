from datetime import datetime
from typing import List

from trade.models import Base, Order, Portfolio, PortfolioVersion
from trade.repositories import TickersRepository, PortfolioVersionsRepository
from trade.repositories.repository_interface import RepositoryInterface


class OrdersRepository(RepositoryInterface):
    def __init__(self, model: Order = Order):
        self.model = model

    def save(self, model: Base) -> Order:
        pass

    def create(self, data: dict) -> Order:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        return Order.create(**data)

    def build_and_create(
        self, symbol_name: str, portfolio_version_id: int, desired_price: float, type: str
    ) -> Order:
        order = self.create(
            {
                "ticker": TickersRepository().get_by_name(symbol_name),
                "portfolio_version": PortfolioVersionsRepository().get_by_id(
                    portfolio_version_id
                ),
                "desired_price": desired_price,
                "status": "created",  # TODO: move to constants
                "type": type
            }
        )
        return order

    def get_by_id(self, id: int) -> Order:
        pass

    def get_orders_by_portfolio(self, portfolio: Portfolio) -> List[Order]:
        result = (
            self.model.select()
            .join(PortfolioVersion)
            .join(Portfolio)
            .where(Portfolio.id == portfolio.id)
            .execute()
        )
        return list(result)
