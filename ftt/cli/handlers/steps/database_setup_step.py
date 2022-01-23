from typing import Optional

from result import Result, Ok

from ftt.cli.application_config_dto import ApplicationConfigDTO
from ftt.handlers.handler.abstract_step import AbstractStep
from ftt.storage import Storage


class DatabaseSetupStep(AbstractStep):
    key = "database_setup"

    @classmethod
    def process(
        cls, application_config_dto: ApplicationConfigDTO
    ) -> Result[ApplicationConfigDTO, Optional[str]]:
        Storage.initialize_database(
            application_name=application_config_dto.application_name,
            environment=application_config_dto.environment,
            root_path=application_config_dto.root_path,
        )
        manager = Storage.storage_manager()
        manager.create_tables(Storage.get_models())

        return Ok()
