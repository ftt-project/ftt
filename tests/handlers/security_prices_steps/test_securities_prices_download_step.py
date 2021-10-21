from datetime import datetime

import pytest
from pandas import DataFrame

from ftt.handlers.security_prices_steps.securities_prices_download_step import (
    SecurityPricesDownloadStep,
)


class TestSecurityPricesDownloadStep:
    @pytest.fixture
    def subject(self):
        return SecurityPricesDownloadStep

    def test_load_securities_historical_prices(self, subject, mocker, security):
        mocker.patch("yfinance.pdr_override")
        mock = mocker.patch("pandas_datareader.data.get_data_yahoo")
        mock.return_value = DataFrame()
        result = subject.process(
            securities=[security],
            start_period=datetime.today(),
            end_period=datetime.today(),
            interval="1d",
        )

        mock.assert_called_once()
        assert result.is_ok()
        assert result.value[security.symbol] is not None
