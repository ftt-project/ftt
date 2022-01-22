import pytest

from ftt.cli.handlers.steps.set_working_directory_step import SetWorkingDirectoryStep


class TestSetWorkingDirectoryStep:
    @pytest.fixture
    def subject(self):
        return SetWorkingDirectoryStep

    def test_process_set_production_working_directory_for_macos(self, subject, application_config_dto):
        result = subject.process()

        assert result.is_ok()