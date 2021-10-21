import os
import pathlib

import pytest

from ftt.handlers.portfolio_config_handler import PortfolioConfigHandler
from ftt.handlers.portfolio_steps.portfolio_config_parser_step import PortfolioConfig


class TestPortfolioConfigHandler:
    @pytest.fixture
    def subject(self):
        return PortfolioConfigHandler()

    @pytest.fixture
    def existing_path(self):
        realpath = pathlib.Path().resolve()
        return os.path.join(realpath, "tests", "fixtures", "portfolio_dummy_config.yml")

    def test_returns_config_object(self, subject, existing_path):
        result = subject.handle(path=existing_path)

        assert result.is_ok()
        assert isinstance(result.value, PortfolioConfig)
