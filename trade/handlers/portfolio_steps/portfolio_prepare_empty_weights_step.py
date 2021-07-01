from typing import List
from result import Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep


class PortfolioPrepareEmptyWeightsStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(cls, securities: List[str]) -> OkErr:
        result = dict(zip(
            securities,
            [0 for _ in securities]
        ))
        return Ok((result, 0,))
