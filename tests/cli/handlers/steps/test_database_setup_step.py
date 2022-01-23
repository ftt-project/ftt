import pytest

from ftt.cli.handlers.steps.database_setup_step import DatabaseSetupStep


class TestDatabaseSetupStep:
    @pytest.fixture
    def subject(self):
        return DatabaseSetupStep

    def test_process_creates_database_sqlite_file_on_first_run(
        self, subject, mocker, application_config_dto
    ):
        initializer = mocker.patch(
            "ftt.cli.handlers.steps.database_setup_step.Storage.initialize_database",
            return_value=False,
        )
        manager = mocker.patch(
            "ftt.cli.handlers.steps.database_setup_step.Storage.storage_manager",
        )
        manager.create_tables.return_value = True

        result = subject.process(application_config_dto=application_config_dto)

        assert result.is_ok()
        assert initializer.call_count == 1
        assert manager.call_count == 1
