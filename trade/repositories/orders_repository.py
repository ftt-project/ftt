from datetime import datetime
from typing import List

from trade.models import Base, Order, Portfolio, PortfolioVersion
from trade.repositories.repository_interface import RepositoryInterface


class OrdersRepository(RepositoryInterface):
    def __init__(self, model: Order = Order):
        self.model = model

    def save(self, model: Base) -> Base:
        pass

    def create(self, data: dict) -> Base:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        return Order.create(**data)

    def get_by_id(self, id: int) -> Base:
        pass

    def get_orders_by_portfolio(self, portfolio: Portfolio) -> List[Order]:
        result = (self.model.select()
                  .join(PortfolioVersion)
                  .join(Portfolio)
                  .where(Portfolio.id == portfolio.id)
                  .execute())
        return list(result)
