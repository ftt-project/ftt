from typing import Final

from result import Ok

from ftt.cli.application_config_dto import ApplicationConfigDTO
from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.logger import Logger


class LoggerSetupStep(AbstractStep):
    key: Final[str] = "logger"

    @classmethod
    def process(cls, application_config_dto: ApplicationConfigDTO):
        Logger(
            name=application_config_dto.application_name,
            environment=application_config_dto.environment,
            root_path=application_config_dto.root_path,
        )

        return Ok()
