from result import Result, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects.weight_dto import WeightDTO
from ftt.storage.models import Weight
from ftt.storage.repositories.weights_repository import WeightsRepository


class OrderWeightsUpdateStep(AbstractStep):
    key = "order_weight"

    @classmethod
    def process(cls, order, dto) -> Result[Weight, str]:
        weight = WeightsRepository.get_by_security_and_portfolio_version(
            security_id=order.security_id,
            portfolio_version_id=order.portfolio_version_id,
        )

        weight = WeightsRepository.update(
            weight, WeightDTO(position=dto.execution_size)
        )

        return Ok(weight)
