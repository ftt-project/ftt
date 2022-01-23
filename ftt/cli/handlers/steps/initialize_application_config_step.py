import os
import pathlib
import platform
from typing import Optional

from result import Ok, Result, Err

from ftt.cli.application_config_dto import ApplicationConfigDTO
from ftt.handlers.handler.abstract_step import AbstractStep


class InitializeApplicationConfigStep(AbstractStep):
    key = "application_config_dto"

    @classmethod
    def process(
        cls, environment: str, application_name: str
    ) -> Result[ApplicationConfigDTO, Optional[str]]:
        dto = ApplicationConfigDTO(
            platform=platform.system(),
            environment=environment,
            application_name=application_name,
            root_path=pathlib.Path(os.path.join(pathlib.Path.home(), ".ftt")),
        )

        if dto.platform not in ["Linux", "Darwin", "Windows"]:
            return Err(f"Unsupported platform: {dto.platform}")

        return Ok(dto)
