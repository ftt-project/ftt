from result import Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.value_objects import SecurityValueObject
from ftt.storage.models import PortfolioVersion
from ftt.storage.repositories.securities_repository import SecuritiesRepository
from ftt.storage.repositories.weights_repository import WeightsRepository


class PortfolioVersionAssociateEmptyWeightsStep(AbstractStep):
    key = "empty_weights"

    @classmethod
    def process(
        cls,
        portfolio_version: PortfolioVersion,
        securities: list[SecurityValueObject],
    ):
        result = []

        for security_dto in securities:
            security = SecuritiesRepository.get_by_name(security_dto.symbol)
            weight = WeightsRepository.upsert(
                {
                    "portfolio_version": portfolio_version,
                    "security": security,
                    "position": 0,
                    "planned_position": 0,
                }
            )
            result.append(weight)

        return Ok(result)
