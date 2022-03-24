import pytest

from ftt.cli.application_config_dto import ApplicationConfigDTO
from ftt.cli.handlers.prepare_environment_handler import PrepareEnvironmentHandler


class TestPrepareEnvironmentHandler:
    @pytest.fixture
    def subject(self):
        return PrepareEnvironmentHandler()

    def test_handle_returns_success(self, subject, mocker):
        initializer = mocker.patch(
            "ftt.cli.handlers.steps.database_setup_step.Storage.initialize_database",
            return_value=False,
        )
        manager = mocker.patch(
            "ftt.cli.handlers.steps.database_setup_step.Storage.storage_manager",
        )
        manager.create_tables.return_value = True

        mkdir = mocker.patch(
            "ftt.cli.handlers.steps.root_folder_setup_step.RootFolderSetupStep.mkdir",
        )

        result = subject.handle(environment="production", application_name="test-ftt")

        assert result.is_ok()
        assert type(result.value) == ApplicationConfigDTO
        assert initializer.call_count == 1
        assert manager.call_count == 1
        assert mkdir.call_count == 1
