from result import Result, Ok

from ftt.brokers.broker_order import BrokerOrder
from ftt.brokers.contract import Contract
from ftt.brokers.ib.ib_config import IBConfig
from ftt.brokers.utils import build_brokerage_service
from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Order


class PlaceOrdersStep(AbstractStep):
    key = "placed_orders"

    @classmethod
    def process(cls, orders: list[Order]) -> Result[id, str]:
        brokerage_service = build_brokerage_service("Interactive Brokers", IBConfig)

        order_ids = []
        for order in orders:
            contract = Contract(
                symbol=order.security.symbol,
                security_type=order.security.quote_type,
                exchange=order.security.exchange,
                currency=order.security.currency,
            )
            broker_order = BrokerOrder(
                action=order.action,
                total_quantity=order.desired_size,
                order_type=order.order_type,
            )
            order_id = brokerage_service.place_order(
                contract=contract, order=broker_order
            )
            # TODO handle error
            order.status = order.__class__.Status.SUBMITTED
            order.save()
            order_ids.append(order_id)

        return Ok(order_ids)
