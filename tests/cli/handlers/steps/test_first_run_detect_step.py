from pathlib import Path

import pytest

from ftt.cli.application_config_dto import ApplicationConfigDTO
from ftt.cli.handlers.steps.first_run_detect_step import FirstRunDetectStep


class TestInitializeApplicationConfigStep:
    @pytest.fixture
    def subject(self):
        return FirstRunDetectStep

    def test_process_returns_true_if_application_is_not_bootstrapped(
        self,
        subject,
    ):
        dto = ApplicationConfigDTO(
            platform="darwin",
            environment="test",
            application_name="ftt-test",
            root_path=Path("/tmp"),
        )
        result = subject.process(dto)

        assert result.is_ok()
        assert result.value.first_run is True

    def test_process_returns_false_if_application_is_bootstrapped(
        self, subject, mocker
    ):
        mocker.patch(
            "ftt.cli.handlers.steps.first_run_detect_step.os.path.isdir",
            return_value=True,
        )
        mocker.patch(
            "ftt.cli.handlers.steps.first_run_detect_step.os.path.isfile",
            return_value=True,
        )
        dto = ApplicationConfigDTO(
            platform="darwin",
            environment="test",
            application_name="ftt-test",
            root_path=Path("/tmp"),
        )
        result = subject.process(dto)

        assert result.is_ok()
        assert result.value.first_run is False
