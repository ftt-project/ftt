import pytest

from ftt.cli.plugin import Plugin


class TestPlugin:
    @pytest.fixture
    def subject(self):
        return Plugin

    @pytest.mark.skip(reason="TODO")
    def test_something(self, subject):
        assert subject.something() == "something"
