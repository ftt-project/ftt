from result import Result, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.value_objects import OrderValueObject
from ftt.storage.models import Order
from ftt.storage.repositories.orders_repository import OrdersRepository


class OrderUpdateStep(AbstractStep):
    key = "updated_order"

    @classmethod
    def process(cls, order: Order, dto: OrderValueObject) -> Result[Order, str]:
        result = OrdersRepository.update(order, dto)
        return Ok(result)
