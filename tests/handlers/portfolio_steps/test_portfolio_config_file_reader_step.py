import os.path
import pathlib

import pytest

from trade.handlers.portfolio_steps.portfolio_config_file_reader import PortfolioConfigFileReaderStep


class TestPortfolioConfigFileReaderStep:
    @pytest.fixture
    def subject(self):
        return PortfolioConfigFileReaderStep

    @pytest.fixture
    def existing_path(self):
        realpath = pathlib.Path().resolve()
        return os.path.join(realpath, "tests", "fixtures", "portfolio_dummy_config.yml")

    @pytest.fixture
    def not_existing_path(self):
        realpath = pathlib.Path().resolve()
        return os.path.join(realpath, "tests", "fixtures", "no_such_config.yml")

    def test_reads_file_and_returns_config(self, subject, existing_path):
        result = subject.process(existing_path)

        assert result.is_ok()
        assert type(result.value) == dict
        assert result.value["name"] == "S&P companies"

    def test_returns_err_if_no_config_found(self, subject, not_existing_path):
        result = subject.process(not_existing_path)

        assert result.is_err()
        assert result.value.strerror == 'No such file or directory'
