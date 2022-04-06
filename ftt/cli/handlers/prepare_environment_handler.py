from ftt.cli.handlers.steps.database_setup_step import DatabaseSetupStep
from ftt.cli.handlers.steps.initialize_application_config_step import (
    InitializeApplicationConfigStep,
)
from ftt.cli.handlers.steps.first_run_detect_step import FirstRunDetectStep
from ftt.cli.handlers.steps.logger_setup_step import LoggerSetupStep
from ftt.cli.handlers.steps.root_folder_setup_step import RootFolderSetupStep
from ftt.cli.handlers.steps.define_expected_working_directory_step import (
    DefineExpectedWorkingDirectoryStep,
)
from ftt.handlers.handler.handler import Handler
from ftt.handlers.handler.return_result import ReturnResult


class PrepareEnvironmentHandler(Handler):
    params = (
        "environment",
        "application_name",
    )

    handlers = [
        (InitializeApplicationConfigStep, "environment", "application_name"),
        (DefineExpectedWorkingDirectoryStep, InitializeApplicationConfigStep.key),
        (FirstRunDetectStep, InitializeApplicationConfigStep.key),
        (RootFolderSetupStep, InitializeApplicationConfigStep.key),
        (DatabaseSetupStep, InitializeApplicationConfigStep.key),
        (LoggerSetupStep, InitializeApplicationConfigStep.key),
        (ReturnResult, InitializeApplicationConfigStep.key),
    ]
