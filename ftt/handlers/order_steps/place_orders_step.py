from result import Result, Ok

from ftt.brokers.contract import Contract
from ftt.brokers.order import Order
from ftt.brokers.utils import build_brokerage_service
from ftt.handlers.handler.abstract_step import AbstractStep


class PlaceOrdersStep(AbstractStep):
    key = "placed_orders"

    @classmethod
    def process(cls, order: Order, contract: Contract) -> Result[id, str]:
        config = {"host": "127.0.0.1", "port": 7497, "client_id": 1234}
        brokerage_service = build_brokerage_service("Interactive Brokers", config)
        order_id = brokerage_service.place_order(contract, order)

        return Ok(order_id)