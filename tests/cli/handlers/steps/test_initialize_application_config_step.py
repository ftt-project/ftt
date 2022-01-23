import pytest

from ftt.cli.handlers.steps.initialize_application_config_step import (
    InitializeApplicationConfigStep,
)


class TestInitializeApplicationConfigStep:
    @pytest.fixture
    def subject(self):
        return InitializeApplicationConfigStep

    def test_process_returns_dto_with_detected_platform_name(self, subject):
        result = subject.process(environment="test", application_name="ftt-test")

        assert result.is_ok()
        assert result.value.platform is not None

    def test_process_returns_err_if_platform_name_is_not_unsupported(
        self, subject, mocker
    ):
        mocker.patch(
            "ftt.cli.handlers.steps.initialize_application_config_step.platform.system",
            return_value="AIX",
        )
        result = subject.process(environment="test", application_name="ftt-test")

        assert result.is_err()
        assert result.value == "Unsupported platform: AIX"
