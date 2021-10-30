import os
import pathlib

import pytest

import ftt
from ftt.handlers.portfolio_config_handler import PortfolioConfigHandler
from ftt.handlers.portfolio_steps.portfolio_config_parser_step import PortfolioConfig


class TestPortfolioConfigHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioConfigHandler()

    def absolute_path(self, file):
        path = os.path.dirname(ftt.__file__)
        path = os.path.join(path, "..", "tests", "fixtures", file)
        return os.path.abspath(path)

    @pytest.fixture
    def existing_path(self):
        return self.absolute_path("portfolio_dummy_config.yml")

    def test_returns_config_object(self, subject, existing_path):
        result = subject.handle(path=existing_path)

        assert result.is_ok()
        assert isinstance(result.value, PortfolioConfig)
