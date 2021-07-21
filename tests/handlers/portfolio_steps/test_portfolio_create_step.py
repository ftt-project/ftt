from datetime import datetime

import pytest

from trade.handlers.portfolio_steps.portfolio_create_step import PortfolioCreateStep
from trade.storage.models.portfolio import Portfolio


class TestPortfolioCreateStep:
    @pytest.fixture
    def subject(self):
        return PortfolioCreateStep

    @pytest.fixture
    def arguments(self):
        return {
            "name": "Example",
            "amount": 10000,
            "period_start": datetime(2021, 1, 1),
            "period_end": datetime(2021, 4, 25),
            "interval": "1wk"
        }

    def test_process(self, subject, arguments):
        result = subject.process(**arguments)
        assert result.is_ok()
        assert type(result.value) == Portfolio
        assert result.value.id is not None

    def test_validates_interval(self, subject, arguments):
        arguments["interval"] = "1w"
        result = subject.process(**arguments)

        assert result.is_err()
        assert result.value == "Interval must be one of ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'] but given 1w."

    def test_validates_period_end(self, subject, arguments):
        arguments["period_end"] = datetime(2020, 12, 1)
        result = subject.process(**arguments)

        assert result.is_err()
        assert result.value == "Period end must be greater than period start but given period start: 2021-01-01 00:00:00 and period_end 2020-12-01 00:00:00"