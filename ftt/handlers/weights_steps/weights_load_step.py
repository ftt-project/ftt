from typing import List, Optional

from result import Ok, Result

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion, Weight
from ftt.storage.repositories.weights_repository import WeightsRepository


class WeightsLoadStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(
        cls, portfolio_version: PortfolioVersion
    ) -> Result[List[Weight], Optional[str]]:
        list = WeightsRepository.get_by_portfolio_version(portfolio_version)

        return Ok(list)
