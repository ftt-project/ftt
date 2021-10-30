import pytest

from ftt.handlers.handler.context import Context


class TestContext:
    @pytest.fixture
    def subject(self):
        return Context

    def test_assigns_values(self, subject):
        assigner = subject(assign=1, to="key")
        input = {}
        result = assigner.process(input)
        assert type(assigner) == Context.Assigner
        assert result.value["key"] == 1
        assert input["key"] == 1

    def test_rename_values(self, subject):
        renamer = subject(rename="old", to="new")
        input = {"old": 1}
        result = renamer.process(input)
        assert type(renamer) == Context.Renamer
        assert result.value["new"] == 1
        assert input["new"] == 1
        assert "old" not in input
