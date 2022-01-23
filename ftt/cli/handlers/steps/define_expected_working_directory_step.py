import os
from pathlib import Path
from typing import Optional

from result import Result, Ok

from ftt.cli.application_config_dto import ApplicationConfigDTO
from ftt.handlers.handler.abstract_step import AbstractStep


class DefineExpectedWorkingDirectoryStep(AbstractStep):
    """
    Set root path for the current system and environment.
    """

    key = "set_working_directory"

    @classmethod
    def process(
        cls, application_config_dto: ApplicationConfigDTO
    ) -> Result[ApplicationConfigDTO, Optional[str]]:
        root_path = cls._environments_system_mapping(
            application_config_dto.environment, application_config_dto.platform
        )
        application_config_dto.root_path = root_path

        return Ok(application_config_dto)

    @classmethod
    def _environments_system_mapping(cls, env, platform):
        import ftt
        from ftt.application import ENVIRONMENT, APPLICATION_NAME
        import pathlib

        unixlike = {
            ENVIRONMENT.production: Path(
                os.path.join((os.path.expanduser("~")), f".{APPLICATION_NAME}")
            ),
            ENVIRONMENT.development: pathlib.Path.joinpath(
                Path(ftt.__file__), Path(".."), Path("..")
            ).resolve(),
            ENVIRONMENT.test: pathlib.Path.joinpath(
                Path(ftt.__file__), Path(".."), Path(".."), Path("tests")
            ).resolve(),
        }

        mapping = {
            "Linux": unixlike,
            "Darwin": unixlike,
            "Windows": {
                ENVIRONMENT.production: Path(
                    os.path.join((os.path.expanduser("~")), f".{APPLICATION_NAME}")
                ),
                ENVIRONMENT.development: pathlib.Path.joinpath(
                    Path(ftt.__file__), Path(".."), Path("..")
                ).resolve(),
                ENVIRONMENT.test: Path(
                    os.path.join((os.path.expanduser("~")), f".{APPLICATION_NAME}")
                ),
            },
        }

        return mapping[platform][env]
