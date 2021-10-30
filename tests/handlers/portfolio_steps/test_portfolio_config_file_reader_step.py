import os.path

import pytest

import ftt
from ftt.handlers.portfolio_steps.portfolio_config_file_reader import (
    PortfolioConfigFileReaderStep,
)


class TestPortfolioConfigFileReaderStep:
    @pytest.fixture
    def subject(self):
        return PortfolioConfigFileReaderStep

    def absolute_path(self, file):
        path = os.path.dirname(ftt.__file__)
        path = os.path.join(path, "..", "tests", "fixtures", file)
        return os.path.abspath(path)

    @pytest.fixture
    def existing_path(self):
        return self.absolute_path("portfolio_dummy_config.yml")

    @pytest.fixture
    def not_existing_path(self):
        return self.absolute_path("not_existing_file.yml")

    def test_reads_file_and_returns_config(self, subject, existing_path):
        result = subject.process(existing_path)

        assert result.is_ok()
        assert type(result.value) == dict
        assert result.value["name"] == "S&P companies"

    def test_returns_err_if_no_config_found(self, subject, not_existing_path):
        result = subject.process(not_existing_path)

        assert result.is_err()
        assert result.value.strerror == "No such file or directory"
