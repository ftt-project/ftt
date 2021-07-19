import datetime

import pandas as pd
import pytest

from trade.handlers.securities_loading_handler import SecuritiesLoadingHandler
from trade.storage.models.security import Security


class TestSecuritiesLoadingHandler:
    @pytest.fixture
    def subject(self):
        return SecuritiesLoadingHandler

    @pytest.fixture(autouse=True)
    def mock_info_requests(self, mocker):
        ticker_mock = mocker.Mock()
        ticker_mock.info = {
            "symbol": "AAPL",
            "quoteType": "EQUITY",
            "sector": "Technology",
            "country": "United States",
            "industry": "Consumer Electronics",
            "currency": "USD",
            "exchange": "NMS",
            "shortName": "Apple Inc.",
            "longName": "Apple Inc.",
        }
        mocker.patch("yfinance.Ticker", return_value=ticker_mock)

    @pytest.fixture(autouse=True)
    def mock_prices_requests(self, mocker):
        mocker.patch("yfinance.pdr_override")
        mock = mocker.patch("pandas_datareader.data.get_data_yahoo")
        mock.return_value = pd.DataFrame(
            data={
                "Adj Close": [124.279999, 125.059998, 123.540001],
                "Close": [124.279999, 125.059998, 123.540001],
                "High": [125.349998, 125.239998, 124.849998],
                "Low": [123.940002, 124.050003, 123.129997],
                "Open": [125.080002, 124.279999, 124.680000],
                "Volume": [67637100, 59278900, 76229200],
            },
            index=pd.DatetimeIndex(
                ["2021-06-01 01:01:01", "2021-06-02 01:01:01", "2021-06-03 01:01:01"]
            ),
        ).rename_axis("Date")

    def test_persists_loaded_securities(self, subject):
        result = subject().handle(
            securities=["AAPL"],
            start_period=datetime.date.today() - datetime.timedelta(days=2),
            end_period=datetime.date.today(),
            interval="1d",
        )

        assert result.is_ok()
        assert type(result.value) == list
        assert len(result.value) == 1
        assert type(result.value[0]) == Security
        assert result.value[0].symbol == "AAPL"

    def test_persist_historical_prices(self, subject):
        result = subject().handle(
            securities=["AAAA"],
            start_period=datetime.date.today() - datetime.timedelta(days=2),
            end_period=datetime.date.today(),
            interval="1d",
        )

        assert len(result.value[0].prices) == 3
