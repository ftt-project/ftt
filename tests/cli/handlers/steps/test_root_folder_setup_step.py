import os
from pathlib import Path

import pytest

from ftt.cli.application_config_dto import ApplicationConfigDTO
from ftt.cli.handlers.steps.root_folder_setup_step import RootFolderSetupStep


class TestRootFolderSetupStep:
    @pytest.fixture
    def subject(self):
        return RootFolderSetupStep

    def test_process_creates_root_folder_on_first_run(
        self, subject, mocker, application_config_dto
    ):
        mkdir_mock = mocker.MagicMock(return_value=True)
        application_config_dto.root_path = mkdir_mock

        result = subject.process(application_config_dto=application_config_dto)

        assert result.is_ok()
        assert mkdir_mock.mkdir.call_count == 1

    def test_process_does_not_create_root_dir_if_not_first_run(
        self, subject, mocker, application_config_dto
    ):
        mkdir = mocker.patch(
            "ftt.cli.handlers.steps.root_folder_setup_step.RootFolderSetupStep.mkdir",
            return_value=True,
        )

        application_config_dto.first_run = False
        result = subject.process(application_config_dto=application_config_dto)

        assert result.is_ok()
        assert mkdir.call_count == 0

    def test_process_returns_error_if_root_dir_already_exists(
        self, subject, mocker, application_config_dto
    ):
        mkdir_mock = mocker.MagicMock(return_value=True)
        mkdir_mock.mkdir.side_effect = OSError()
        application_config_dto.root_path = mkdir_mock

        result = subject.process(application_config_dto=application_config_dto)

        assert result.is_err()
        assert mkdir_mock.mkdir.call_count == 1
