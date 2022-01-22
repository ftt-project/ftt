import pytest

from ftt.cli.application import Application


class TestApplication:
    @pytest.fixture
    def subject(self):
        return Application

    @pytest.mark.skip(reason="TODO")
    def test_exit_successfully(self, mocker, subject):
        pass
