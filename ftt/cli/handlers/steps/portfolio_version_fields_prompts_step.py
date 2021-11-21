from decimal import Decimal

from prompt_toolkit import prompt
from result import OkErr, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO


class PortfolioVersionFieldsPromptsStep(AbstractStep):
    key = "portfolio_version_dto"

    @classmethod
    def process(cls, defaults: PortfolioVersionDTO = PortfolioVersionDTO()) -> OkErr:
        dto = PortfolioVersionDTO(
            value=Decimal(prompt("Account value: ", default=str(defaults.value or ""))),
            period_start=prompt("Period start: ", default=defaults.period_start or ""),
            period_end=prompt("Period end: ", default=defaults.period_end or ""),
            interval=prompt("Interval: ", default=defaults.interval or ""),
        )

        return Ok(dto)
