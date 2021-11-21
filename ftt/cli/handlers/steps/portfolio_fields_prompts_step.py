from prompt_toolkit import prompt
from result import OkErr, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects.portfolio_dto import PortfolioDTO


class PortfolioFieldsPromptsStep(AbstractStep):
    key = "portfolio_dto"

    @classmethod
    def process(cls) -> OkErr:
        dto = PortfolioDTO(name=prompt("Portfolio name: "),)

        return Ok(dto)
