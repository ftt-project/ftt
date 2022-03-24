from datetime import datetime
from decimal import Decimal
from typing import Optional

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.validation import Validator
from result import Ok, Result

from ftt.cli.token import Token
from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO
from ftt.storage.models.portfolio_version import ACCEPTABLE_INTERVALS


class PortfolioVersionFieldsPromptsStep(AbstractStep):
    key = "portfolio_version_dto"

    @classmethod
    def process(
        cls, defaults: PortfolioVersionDTO = PortfolioVersionDTO()
    ) -> Result[PortfolioVersionDTO, Optional[str]]:
        value = cls.prompt_value(defaults)
        period_start = cls.prompt_period(
            defaults.period_start, "Period start", datetime(1950, 1, 1)
        )
        period_end = cls.prompt_period(defaults.period_end, "Period end", period_start)
        interval = cls.prompt_interval(defaults)

        dto = PortfolioVersionDTO(
            value=value,
            period_start=period_start,
            period_end=period_end,
            interval=interval,
        )

        return Ok(dto)

    @staticmethod
    def prompt_value(defaults) -> Decimal:
        def is_valid_value(text):
            return len(text) > 0

        validator = Validator.from_callable(
            is_valid_value,
            error_message="Not a valid account value (The number must be bigger than 0).",
            move_cursor_to_end=True,
        )

        result = prompt(
            "Account value: ",
            validator=validator,
            default=str(defaults.value or ""),
            placeholder=PygmentsTokens([(Token.Placeholder, "0.00")]),
        )

        return Decimal(result)

    @staticmethod
    def period_validator(valid_lower_period):
        def is_valid_date(text):
            try:
                return datetime.strptime(text, "%Y-%m-%d") > valid_lower_period
            except ValueError:
                return False

        return Validator.from_callable(
            is_valid_date,
            error_message="Not a valid date value (use format YYYY-MM-DD, the date "
            f"must come after {datetime.strftime(valid_lower_period, '%Y-%m-%d')}).",
            move_cursor_to_end=True,
        )

    @classmethod
    def prompt_period(cls, defaults, prompt_message, valid_lower_period) -> datetime:
        result = prompt(
            f"{prompt_message}: ",
            validator=cls.period_validator(valid_lower_period),
            default=str(defaults or ""),
            placeholder=PygmentsTokens([(Token.Placeholder, "YYYY-MM-DD")]),
        )

        return datetime.strptime(result, "%Y-%m-%d")

    @staticmethod
    def prompt_interval(defaults) -> str:
        def is_valid_interval(text):
            return text in ACCEPTABLE_INTERVALS

        validator = Validator.from_callable(
            is_valid_interval,
            error_message=f"Not a valid interval value (Valid intervals are: {ACCEPTABLE_INTERVALS}).",
            move_cursor_to_end=True,
        )

        result = prompt(
            "Interval: ",
            validator=validator,
            default=str(defaults.interval or ""),
            placeholder=PygmentsTokens(
                [(Token.Placeholder, f"{ACCEPTABLE_INTERVALS}")]
            ),
        )

        return result
