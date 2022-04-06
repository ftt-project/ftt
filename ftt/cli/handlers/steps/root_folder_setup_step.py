from pathlib import Path
from typing import Optional

from result import Result, Ok, Err

from ftt.cli.application_config_dto import ApplicationConfigDTO
from ftt.handlers.handler.abstract_step import AbstractStep


class RootFolderSetupStep(AbstractStep):
    key = "root_folder_setup"

    @classmethod
    def process(
        cls, application_config_dto: ApplicationConfigDTO
    ) -> Result[ApplicationConfigDTO, Optional[str]]:
        if application_config_dto.first_run:
            try:
                cls.mkdir(application_config_dto.root_path)
                return Ok(application_config_dto)
            except FileExistsError:
                pass
            except OSError as error:
                return Err(repr(error))

        return Ok(application_config_dto)

    @classmethod
    def mkdir(cls, root_path: Path):
        root_path.mkdir()
