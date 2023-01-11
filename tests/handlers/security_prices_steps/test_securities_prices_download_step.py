import pandas as pd
import pytest

from ftt.handlers.security_prices_steps.securities_prices_download_step import (
    SecurityPricesDownloadStep,
)
from ftt.storage import schemas


class TestSecurityPricesDownloadStep:
    @pytest.fixture
    def subject(self):
        return SecurityPricesDownloadStep

    def test_load_securities_historical_prices(
        self,
        subject,
        security,
        portfolio,
        mock_external_historic_data_requests,
    ):
        result = subject.process(
            securities=[schemas.Security.from_orm(security)],
            portfolio=schemas.Portfolio.from_orm(portfolio),
        )

        mock_external_historic_data_requests.assert_called_once()
        assert result.is_ok()
        assert result.value[security.symbol] is not None

    def test_process_download_historical_prices_mode_always(
        self,
        subject,
        security,
        portfolio,
        mock_external_historic_data_requests,
    ):
        result = subject.process(
            securities=[schemas.Security.from_orm(security)],
            portfolio=schemas.Portfolio.from_orm(portfolio),
            mode="always",
        )

        mock_external_historic_data_requests.assert_called_once()
        assert result.is_ok()
        assert result.value[security.symbol] is not None

    def test_process_download_historical_prices_model_missing(
        self,
        subject,
        security,
        portfolio,
        security_price_factory,
        mock_external_historic_data_requests,
    ):
        # assuming portfolio.interval is 5min
        date_range = pd.date_range(
            start=portfolio.period_start, end=portfolio.period_end, freq="5min"
        )
        for index, value in date_range.to_series().items():
            _ = security_price_factory(
                security=security,
                dt=value.to_pydatetime(),
                interval=portfolio.interval,
                close=value.day,
            )

        result = subject.process(
            securities=[schemas.Security.from_orm(security)],
            portfolio=schemas.Portfolio.from_orm(portfolio),
            mode="on_missing",
        )

        mock_external_historic_data_requests.assert_not_called()
        assert result.is_ok()
        assert result.value == {}
