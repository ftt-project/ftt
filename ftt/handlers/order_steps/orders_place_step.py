from result import Result, Ok

from ftt.brokers.broker_order import BrokerOrder
from ftt.brokers.contract import Contract
from ftt.brokers.ib.ib_config import IBConfig
from ftt.brokers.utils import build_brokerage_service
from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.logger import Logger
from ftt.storage.models import Order


class OrdersPlaceStep(AbstractStep):
    key = "placed_orders"

    @classmethod
    def process(cls, orders: list[Order]) -> Result[list[Order], str]:
        brokerage_service = build_brokerage_service("Interactive Brokers", IBConfig)

        order_ids = []
        for idx, order in enumerate(orders):
            contract = Contract(
                symbol=order.security.symbol,
                # security_type=order.security.quote_type,
                # TODO: use security.quote_type instead of hardcoded "STK" value
                # The problem is that security is "equity",
                # that is not correct https://www.educba.com/stock-vs-equities/
                security_type="STK",
                # exchange=order.security.exchange,
                exchange="SMART",
                currency=order.security.currency,
            )
            broker_order = BrokerOrder(
                action=order.action,
                total_quantity=order.desired_size,
                order_type=order.order_type,
            )
            order_id = brokerage_service.place_order(
                contract=contract,
                order=broker_order,
                next_order_id=order.id,
            )
            Logger.info(f"{__name__}::process placed order_id={order_id}")
            # TODO handle error
            if order_id is not None:
                order.status = order.__class__.Status.SUBMITTED
                order.external_id = order_id
                order.save()
                order_ids.append(order_id)
            else:
                # TODO Handle error
                print(f"Error placing order {order.id}")
                pass

        return Ok(orders)
