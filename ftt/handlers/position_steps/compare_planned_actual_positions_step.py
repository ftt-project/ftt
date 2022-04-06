from typing import List, Iterable

from result import Result, Ok

from ftt.brokers.contract import Contract
from ftt.brokers.broker_order import BrokerOrder, OrderAction, OrderType
from ftt.brokers.position import Position
from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import Weight


class ComparePlannedActualPositionsStep(AbstractStep):
    """
    Compares planned positions saved in Weights with given a given positions.
    Returns a combination of Order and Contract that is enough to represent the difference for order placement
    """

    key = "order_candidates"

    @classmethod
    def process(
        cls, weights: List[Weight], open_positions: List[Position]
    ) -> Result[list[tuple[BrokerOrder, Contract]], str]:
        """
        Parameters
        ----------
        weights : array_like
            List of Weight models to compare
        open_positions : array_like
            Lit of Position value objects

        Returns
        -------
        list
            Returns a list of contact, order that could be used for order placement
            in the format List<Tuple<Contract, Order>> where Contract and Order
            are value objects. Contract contains information about security order
            action that must be applied to a contract.
        """
        normalized_by_symbol_planned_positions = cls._normalize_positions(
            open_positions
        )
        normalized_by_symbol_weights = cls._normalize_weights(weights)

        symbols_collection: Iterable = list(
            normalized_by_symbol_planned_positions.keys()
        ) + list(normalized_by_symbol_weights.keys())
        symbols_collection = set(symbols_collection)

        result: list = []
        for symbol in symbols_collection:
            weight = normalized_by_symbol_weights.get(symbol)
            position = normalized_by_symbol_planned_positions.get(symbol)
            if weight and position:
                if weight < position:
                    result.append(
                        (
                            BrokerOrder(
                                action=OrderAction.SELL,
                                total_quantity=float(position - weight),
                                order_type=OrderType.MARKET,
                            ),
                            Contract(
                                symbol=symbol,
                                security_type=Contract.SecurityType.STOCK,
                            ),
                        )
                    )
                elif weight > position:
                    result.append(
                        (
                            BrokerOrder(
                                action=OrderAction.BUY,
                                total_quantity=float(weight - position),
                                order_type=OrderType.MARKET,
                            ),
                            Contract(
                                symbol=symbol,
                                security_type=Contract.SecurityType.STOCK,
                            ),
                        )
                    )
                else:
                    # no action required as planned position (in weights) is equal to actual position (in positions)
                    pass
            elif weight and not position:
                result.append(
                    (
                        BrokerOrder(
                            action=OrderAction.BUY,
                            total_quantity=float(weight),
                            order_type=OrderType.MARKET,
                        ),
                        Contract(
                            symbol=symbol,
                            security_type=Contract.SecurityType.STOCK,
                        ),
                    )
                )
            else:
                # no action required
                # we could have more open positions in the system that do not belong to current portfolio's weights,
                # and we ignore them
                pass

        return Ok(result)

    @staticmethod
    def _normalize_positions(positions: List[Position]) -> dict[str, float]:
        return {position.contract.symbol: position.position for position in positions}

    @staticmethod
    def _normalize_weights(weights: List[Weight]) -> dict[str, float]:
        return {weight.security.symbol: weight.planned_position for weight in weights}
