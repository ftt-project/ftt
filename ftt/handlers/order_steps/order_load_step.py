from result import Result, Err, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Order
from ftt.storage.repositories.orders_repository import OrdersRepository


class OrderLoadStep(AbstractStep):
    key = "order"

    @classmethod
    def process(cls, order_id: int) -> Result[Order, str]:
        order = OrdersRepository.get_by_id(order_id)
        if order is None:
            return Err("Order not found")

        return Ok(order)
