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

    def test_loads_security_prices(
        self,
        subject,
        security,
        portfolio,
        security_price_factory,
        portfolio_version_factory,
        weight_factory,
    ):
        _ = security_price_factory(
            security=security, interval="1d", dt=datetime.datetime(2020, 1, 1)
        )
        portfolio_version = portfolio_version_factory(
            portfolio=portfolio, interval="1d"
        )
        _ = weight_factory(security=security, portfolio_version=portfolio_version)

        result = subject.process(
            portfolio_version=portfolio_version,
            portfolio_version_securities=[security],
        )

        assert result.is_ok()
        assert len(result.value) == 1
        assert type(result.value) == DataFrame
        assert security.symbol in result.value.columns
