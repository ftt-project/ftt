import os.path
from pathlib import Path

import pytest

from ftt.cli.handlers.steps.define_expected_working_directory_step import (
    DefineExpectedWorkingDirectoryStep,
)


class TestDefineExpectedWorkingDirectoryStep:
    @pytest.fixture
    def subject(self):
        return DefineExpectedWorkingDirectoryStep

    def test_process_for_macos_production(self, subject, application_config_dto):
        from ftt.application import ENVIRONMENT

        application_config_dto.environment = ENVIRONMENT.production
        application_config_dto.platform = "Darwin"

        result = subject.process(application_config_dto=application_config_dto)

        assert result.is_ok()
        assert result.value.root_path == Path(
            os.path.join((os.path.expanduser("~")), ".ftt")
        )

    def test_process_for_macos_development(self, subject, application_config_dto):
        from ftt.application import ENVIRONMENT

        application_config_dto.environment = ENVIRONMENT.development
        application_config_dto.platform = "Darwin"

        result = subject.process(application_config_dto=application_config_dto)

        assert result.is_ok()
        assert "/ftt" in str(result.value.root_path)

    def test_process_for_macos_test(self, subject, application_config_dto):
        from ftt.application import ENVIRONMENT

        application_config_dto.environment = ENVIRONMENT.test
        application_config_dto.platform = "Darwin"

        result = subject.process(application_config_dto=application_config_dto)

        assert result.is_ok()
        assert "/ftt/tests" in str(result.value.root_path)

    def test_process_for_linux_production(self, subject, application_config_dto):
        from ftt.application import ENVIRONMENT

        application_config_dto.environment = ENVIRONMENT.production
        application_config_dto.platform = "Linux"

        result = subject.process(application_config_dto=application_config_dto)

        assert result.is_ok()
        assert result.value.root_path == Path(
            os.path.join((os.path.expanduser("~")), ".ftt")
        )

    def test_process_for_linux_development(self, subject, application_config_dto):
        from ftt.application import ENVIRONMENT

        application_config_dto.environment = ENVIRONMENT.development
        application_config_dto.platform = "Darwin"

        result = subject.process(application_config_dto=application_config_dto)

        assert result.is_ok()
        assert "/ftt" in str(result.value.root_path)

    def test_process_for_linux_test(self, subject, application_config_dto):
        from ftt.application import ENVIRONMENT

        application_config_dto.environment = ENVIRONMENT.test
        application_config_dto.platform = "Darwin"

        result = subject.process(application_config_dto=application_config_dto)

        assert result.is_ok()
        assert "/ftt/tests" in str(result.value.root_path)

    @pytest.mark.skip(reason="Not implemented")
    def test_process_for_windows_production(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_process_for_windows_development(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_process_for_windows_test(self):
        pass
