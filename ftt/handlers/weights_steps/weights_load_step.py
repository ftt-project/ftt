from result import Ok, OkErr

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.weights_repository import WeightsRepository


class WeightsLoadStep(AbstractStep):
    key = "weights"

    @classmethod
    def process(cls, portfolio_version: PortfolioVersion) -> OkErr:
        list = WeightsRepository.get_by_portfolio_version(portfolio_version)

        return Ok(list)
