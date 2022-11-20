from datetime import datetime

import pytest
from pandas import DataFrame

from ftt.handlers.security_prices_steps.securities_prices_download_step import (
    SecurityPricesDownloadStep,
)
from ftt.storage.value_objects import PortfolioVersionValueObject


class TestSecurityPricesDownloadStep:
    @pytest.fixture
    def subject(self):
        return SecurityPricesDownloadStep

    @pytest.fixture
    def portfolio_version_dto(self):
        return PortfolioVersionValueObject(
            period_start=datetime.today(),
            period_end=datetime.today(),
            interval="1d",
        )

    def test_load_securities_historical_prices(
        self,
        subject,
        mocker,
        security,
        portfolio_version_dto,
        mock_external_historic_data_requests,
    ):
        result = subject.process(
            securities=[security],
            portfolio_version=portfolio_version_dto,
        )

        mock_external_historic_data_requests.assert_called_once()
        assert result.is_ok()
        assert result.value[security.symbol] is not None
