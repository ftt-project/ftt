import pathlib

import pytest

from ftt.cli.handlers.define_example_config_path_step import DefineExampleConfigPathStep


class TestDefineExampleConfigPathStep:
    @pytest.fixture
    def subject(self):
        return DefineExampleConfigPathStep

    def test_process_returns_path_to_example_config_file(self, subject):
        result = subject.process(pathlib.Path("xyz"))

        expected_sub_path = pathlib.Path.joinpath(
            pathlib.Path("xyz"),
            pathlib.Path("config"),
            pathlib.Path("example_portfolio.yml"),
        )

        assert str(expected_sub_path) in str(result.value)
