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

    def test_returns_config_object(self, subject):
        result = subject.handle()

        assert result.is_ok()
        assert isinstance(result.value, PortfolioConfig)
