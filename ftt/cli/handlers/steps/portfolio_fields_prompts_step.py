from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator
from result import OkErr, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects.portfolio_dto import PortfolioDTO


class PortfolioFieldsPromptsStep(AbstractStep):
    key = "portfolio_dto"

    @classmethod
    def process(cls) -> OkErr:
        name = cls.prompt_name()
        dto = PortfolioDTO(name=name,)

        return Ok(dto)

    @staticmethod
    def prompt_name() -> str:
        def is_valid_name(text):
            return len(text) > 0

        validator = Validator.from_callable(
            is_valid_name,
            error_message="Not a valid name (Must be longer than 0).",
            move_cursor_to_end=True,
        )

        return prompt("Portfolio name: ", validator=validator)