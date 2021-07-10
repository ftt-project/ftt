from typing import List

from result import Ok, OkErr

from trade.handlers.handler.abstract_step import AbstractStep
from trade.handlers.weights_steps.weights_calculate_step import WeightsCalculateStepResult


class PortfolioPrepareEmptyWeightsStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(cls, securities: List[str]) -> OkErr:
        result = dict(zip(securities, [0 for _ in securities]))
        weights = WeightsCalculateStepResult(allocation=result, leftover=0, expected_annual_return=0, annual_volatility=0, sharpe_ratio=0)
        return Ok(weights)
