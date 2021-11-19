from prompt_toolkit import prompt
from result import OkErr, Ok

from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.data_objects.portfolio_version_dto import PortfolioVersionDTO


class PortfolioVersionFieldsPromptsStep(AbstractStep):
    key = "prompt_answers"

    @classmethod
    def process(cls, defaults: PortfolioVersionDTO = PortfolioVersionDTO()) -> OkErr:
        params = {
            "value": prompt("Account value: ", default=defaults.value),
            "period_start": prompt("Period start: ", default=defaults.period_start),
            "period_end": prompt("Period end: ", default=defaults.period_end),
            "interval": prompt("Interval: ", default=defaults.interval),
        }

        return Ok(PortfolioVersionDTO(**params))
