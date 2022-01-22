from unittest.mock import call

import pytest

from ftt.cli.application import Application


class TestApplication:
    @pytest.fixture
    def subject(self):
        return Application

    def test_exit_successfully(self, mocker, subject):
        sys = mocker.patch("ftt.cli.application.sys")
        sys.argv = ["__main__.py", "--local"]
        sys.exit.return_value = None

        nubia = mocker.patch("ftt.cli.application.Nubia")
        nubia.start_interactive.result = 0

        subject.initialize_and_run()

        assert nubia.called

    # def test_checks_if_application_is_initialized_already(self, subject, mocker):
    #     # in context
    #     nubia = mocker.patch('ftt.cli.application.Nubia')
    #
    #     Application.initialize_and_run()
    #
    #     assert not nubia.called

    # def test_initialize_application_in_the_first_time(self, subject, mocker):
    #     # in context
    #     nubia = mocker.patch('ftt.cli.application.Nubia')
    #
    #     Application.initialize_and_run()
    #
    #     assert not nubia.called
    #
    # def test_prints_version_and_exit_if_version_flag_is_passed(self, subject, mocker):
    #     # in plugin
    #     sys = mocker.patch('ftt.cli.application.sys')
    #     sys.argv = ['__main__.py', '--version', '--dev']
    #     sys.exit.return_value = None
    #
    #     nubia = mocker.patch('ftt.cli.application.Nubia')
    #
    #     subject.initialize_and_run()
    #
    #     assert not nubia.called
    #     assert sys.method_calls == [call.exit(0)]
