from datetime import datetime

import pytest

from ftt.handlers.portfolio_steps.portfolio_config_parser_step import (
    PortfolioConfigParserStep,
)


class TestPortfolioConfigParserStep:
    @pytest.fixture
    def subject(self):
        return PortfolioConfigParserStep

    @pytest.fixture
    def correct_raw_config(self):
        return {
            "name": "test",
            "symbols": ["AA", "BB"],
            "budget": 1000,
            "period_start": "2020-01-01",
            "period_end": "2020-01-01",
            "interval": "1d",
        }

    @pytest.fixture
    def incorrect_raw_config(self):
        return {}

    def test_returns_config(self, subject, correct_raw_config):
        result = subject.process(correct_raw_config)

        assert result.is_ok()
        assert isinstance(result.value.symbols, list)
        assert isinstance(result.value.period_start, datetime)
        assert isinstance(result.value.period_end, datetime)

    def test_returns_error_on_malformed_config(self, subject, incorrect_raw_config):
        result = subject.process(incorrect_raw_config)

        assert result.is_err()
        assert type(result.value) == list
        assert "`name` is missing from config" in result.value
