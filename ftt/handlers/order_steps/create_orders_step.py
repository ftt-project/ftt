from result import Result, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Order, PortfolioVersion, Portfolio, Weight, Security


class CreateOrdersStep(AbstractStep):
    key = "orders"

    @classmethod
    def process(
        cls,
        order_candidates: list,
        weights: list[Weight],
        portfolio: Portfolio,
        portfolio_version: PortfolioVersion,
    ) -> Result[list[Order], str]:
        securities_by_symbol = cls._securities_by_symbol(weights)

        for broker_order, contract in order_candidates:
            order = Order.create(
                action=broker_order.action,
                order_type=broker_order.order_type,
                portfolio=portfolio,
                portfolio_version=portfolio_version,
                security=securities_by_symbol.get(contract.symbol),
                desired_size=broker_order.total_quantity,
                order_status=Order.Status.CREATED,
            )
            order.save()

        return Ok(order)

    @staticmethod
    def _securities_by_symbol(weights: list[Weight]) -> dict[str, Security]:
        securities_by_symbol = {}
        for weight in weights:
            securities_by_symbol[weight.security.symbol] = weight.security
        return securities_by_symbol
