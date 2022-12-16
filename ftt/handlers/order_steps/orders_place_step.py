from result import Result, Ok, as_result

from ftt.brokers.brokerage_service import BrokerageService
from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.logger import Logger
from ftt.storage import schemas
from ftt.storage.models import Order
from ftt.storage.repositories.orders_repository import OrdersRepository


class OrdersPlaceStep(AbstractStep):
    key = "placed_orders"

    @classmethod
    def process(
        cls, orders: list[schemas.Order], brokerage_service: BrokerageService
    ) -> Result[list[Order], str]:
        order_ids = []
        for idx, order in enumerate(orders):
            contract = schemas.Contract(
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
            broker_order = schemas.BrokerOrder(
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

                update = as_result(Exception)(OrdersRepository.update)
                result = update(order)

                order_ids.append(result.unwrap().external_id)
            else:
                # TODO Handle error
                Logger.info(f"Error placing order {order.id}")
                pass

        return Ok(orders)
