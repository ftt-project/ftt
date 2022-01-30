import pathlib

import pytest

from ftt.cli.handlers.steps.define_package_path_step import DefinePackagePathStep


class TestDefinePackagePathStep:
    @pytest.fixture
    def subject(self):
        return DefinePackagePathStep

    def test_process_returns_root_of_the_package(self, subject):
        result = subject.process()

        expected_sub_path = pathlib.Path("ftt")

        assert result.is_ok()
        assert str(expected_sub_path) in str(result.value)
