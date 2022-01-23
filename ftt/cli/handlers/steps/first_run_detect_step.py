import os
from typing import Optional

from result import Result, Ok

from ftt.cli.application_config_dto import ApplicationConfigDTO
from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage.storage_manager import StorageManager


class FirstRunDetectStep(AbstractStep):
    key = "first_run_detect"

    @classmethod
    def process(
        cls, application_config_dto: ApplicationConfigDTO
    ) -> Result[ApplicationConfigDTO, Optional[str]]:
        db_file_present = not os.path.isdir(
            application_config_dto.root_path
        ) or not os.path.isfile(
            StorageManager.database_path(
                application_config_dto.root_path,
                application_config_dto.application_name,
                application_config_dto.environment,
            )
        )

        application_config_dto.first_run = db_file_present

        return Ok(application_config_dto)
