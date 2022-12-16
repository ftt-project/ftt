from result import Result, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas
from ftt.storage.models import Weight, Security
from ftt.storage.repositories.orders_repository import OrdersRepository


class OrdersCreateStep(AbstractStep):
    key = "orders"

    @classmethod
    def process(
        cls,
        calculated_position_differences: list,
        weights: list[schemas.Weight],
        portfolio: schemas.Portfolio,
        portfolio_version: schemas.PortfolioVersion,
    ) -> Result[list[schemas.Order], str]:
        securities_by_symbol = cls._securities_by_symbol(weights)
        weights_by_symbol = cls._weights_by_symbol(weights)

        orders = []
        for position_difference in calculated_position_differences:
            # TODO use repository
            if position_difference.actual_position_difference.SMALLER:
                action = schemas.Order.OrderAction.BUY
            else:
                action = schemas.Order.OrderAction.SELL

            order_type = schemas.Order.OrderType.MARKET

            result = OrdersRepository.create(
                schemas.Order(
                    action=action,
                    order_type=order_type,
                    portfolio=portfolio,
                    portfolio_version=portfolio_version,
                    security=securities_by_symbol[position_difference.symbol],
                    weight=weights_by_symbol.get(position_difference.symbol),
                    desired_size=position_difference.delta,
                    status=schemas.Order.Status.CREATED,
                )
            )
            orders.append(result)

        return Ok(orders)

    @staticmethod
    def _securities_by_symbol(weights: list[Weight]) -> dict[str, Security]:
        securities_by_symbol = {}
        for weight in weights:
            securities_by_symbol[weight.security.symbol] = weight.security
        return securities_by_symbol

    @staticmethod
    def _weights_by_symbol(weights: list[Weight]) -> dict[str, Weight]:
        weights_by_symbol = {}
        for weight in weights:
            weights_by_symbol[weight.security.symbol] = weight
        return weights_by_symbol
