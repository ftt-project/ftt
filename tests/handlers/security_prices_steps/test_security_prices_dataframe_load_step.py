import datetime
from pandas import DataFrame

import pytest

from ftt.handlers.security_prices_steps.security_prices_dataframe_load_step import (
    SecurityPricesDataframeLoadStep,
)


class TestSecurityPricesDataframeLoadStep:
    @pytest.fixture
    def subject(self):
        return SecurityPricesDataframeLoadStep

    def test_loads_security_prices(self, subject, security, security_price):
        result = subject.process(
            securities=[security],
            start_period=datetime.date.today() - datetime.timedelta(days=1),
            end_period=datetime.datetime.now(),
            interval="5m",
        )

        assert result.is_ok()
        assert len(result.value) == 1
        assert type(result.value) == DataFrame
        assert security.symbol in result.value.columns
