from typing import List, Iterable

from result import Result, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import schemas


class ComparePlannedActualPositionsStep(AbstractStep):
    """
    Compares planned positions saved in Weights with given a given positions.
    Returns a combination of Order and Contract that is enough to represent the difference for order placement
    """

    key = "calculated_position_differences"

    @classmethod
    def process(
        cls, weights: list[schemas.Weight], open_positions: list[schemas.Position]
    ) -> Result[list[schemas.CalculatedPositionDifference], str]:
        """
        Parameters
        ----------
        weights : array_like
            List of schemas.Weight models to compare
        open_positions : array_like
            Lit of schemas.Position value objects

        Returns
        -------
        list
            Returns a list of schemas.CalculatedPositionDifference,
            that contains all important information on further recommended actions.
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
                        schemas.CalculatedPositionDifference(
                            symbol=symbol,
                            actual_position_difference=schemas.CalculatedPositionDifference.Difference.BIGGER,
                            planned_position=weight,
                            actual_position=position,
                            delta=float(position - weight),
                        )
                    )
                elif weight > position:
                    result.append(
                        schemas.CalculatedPositionDifference(
                            symbol=symbol,
                            actual_position_difference=schemas.CalculatedPositionDifference.Difference.SMALLER,
                            planned_position=weight,
                            actual_position=position,
                            delta=float(weight - position),
                        )
                    )
                else:
                    # no action required as planned position (in weights) is equal to actual position (in positions)
                    pass
            elif weight and not position:
                result.append(
                    schemas.CalculatedPositionDifference(
                        symbol=symbol,
                        actual_position_difference=schemas.CalculatedPositionDifference.Difference.SMALLER,
                        planned_position=weight,
                        actual_position=0,
                        delta=float(weight),
                    )
                )
            else:
                # no action required
                # we could have more open positions in the system that do not belong to current portfolio's weights,
                # and we ignore them
                pass

        return Ok(result)

    @staticmethod
    def _normalize_positions(positions: List[schemas.Position]) -> dict[str, float]:
        return {
            position.contract.symbol: position.position
            for position in positions
            if position.contract
        }

    @staticmethod
    def _normalize_weights(weights: List[schemas.Weight]) -> dict[str, float]:
        return {
            weight.security.symbol: weight.planned_position
            for weight in weights
            if weight.security and weight.security.symbol
        }
